import asyncio
import logging
from typing import Dict, Any

from core.stock_price.finnhub_schema import CompanyProfile, StockQuote
from domain.trade.trade_repo import TradeRepo
from domain.trade.trade_schema import (
    TradeCreate,
    TradeUpdate,
    TradeResponse,
)
from domain.scale_plan.scale_plan_schema import ScalePlanCreate
from domain.annotation.annotation_repo import AnnotationRepo
from database.models import (
    Annotation,
    Trade,
    AnnotationType,
    TradeStatus,
    ScalePlan,
    PlanType,
    TradeType,
)
from fastapi import HTTPException, status
from core.stock_price.finnhub_service import FinnhubService


class TradeService:
    def __init__(
        self,
        repo: TradeRepo,
        annotation_repo: AnnotationRepo,
        finnhub_service: FinnhubService,
    ):
        self.repo = repo
        self.annotation_repo = annotation_repo
        self.finnhub_service = finnhub_service

    async def get_company_profile(self, symbol: str) -> CompanyProfile | None:
        return await self.finnhub_service.get_company_profile(symbol)

    async def get_all_trades(self) -> list[TradeResponse]:
        """Get all trades with current market data."""
        # Get all trades from the repository
        db_trades = await self.repo.get_all_trades()

        if not db_trades:
            return []

        # Extract unique symbols for market data lookup (only for active trades)
        symbols = list(
            {
                trade.symbol
                for trade in db_trades
                if trade.symbol
                and trade.status in (TradeStatus.OPEN, TradeStatus.WATCHING)
            }
        )

        # Early return if no symbols to lookup
        if not symbols:
            return [TradeResponse.model_validate(trade) for trade in db_trades]

        price_map: Dict[str, StockQuote] = {}
        profile_map: Dict[str, CompanyProfile] = {}

        try:
            price_result, profile_result = await asyncio.gather(
                self._get_price_map(symbols),
                self._get_profile_map(symbols),
                return_exceptions=True,
            )

            if isinstance(price_result, Exception):
                logging.warning(f"Failed to fetch prices: {price_result}")
                price_map = {}
            else:
                price_map = price_result

            if isinstance(profile_result, Exception):
                logging.warning(f"Failed to fetch profiles: {profile_result}")
                profile_map = {}
            else:
                profile_map = profile_result

        except Exception as e:
            logging.error(f"Error fetching market data: {e}")
            price_map = profile_map = {}

        trades = []
        for trade in db_trades:
            trade_data = self._enrich_trade(trade, price_map, profile_map)

            trades.append(TradeResponse.model_validate(trade_data))

        return trades

    async def get_live_trade_by_id(self, live_trade_id: str) -> TradeResponse | None:
        return await self.repo.get_trade_by_id(live_trade_id)

    async def create_trade(self, trade: TradeCreate) -> TradeResponse:
        profile = await self.finnhub_service.get_company_profile(trade.symbol)
        if not profile:
            raise HTTPException(
                status_code=404, detail=f"Stock not found for symbol {trade.symbol}"
            )
        payload = self._build_watchlist_payload(trade)
        # Create LiveTrade instance
        trade_instance = Trade(**payload)

        # Create the trade
        result = await self.repo.create_trade(trade_instance)

        return result

    async def update_trade(
        self, trade_id: str, payload: TradeUpdate
    ) -> TradeResponse | None:
        return await self.repo.update_trade(trade_id, payload)

    async def replace_trade(self, trade_id: str, payload: TradeCreate) -> TradeResponse:
        """Replace an existing trade with new data while preserving certain fields."""
        trade_update_data = payload.model_dump()
        trade_update = TradeUpdate(**trade_update_data)

        result = await self.repo.replace_trade(trade_id, trade_update)

        # Enrich the result with current market data if it's an active trade
        if result.symbol and result.status in (TradeStatus.OPEN, TradeStatus.WATCHING):
            enriched_result = await self._enrich_single_trade(result)
            return enriched_result

        return TradeResponse.model_validate(result)

    async def invalidate_trade(self, trade_id: str) -> None:
        trade = await self.repo.get_trade_by_id(trade_id)
        if not trade:
            raise HTTPException(status_code=404, detail="Trade not found")
        if trade.status != TradeStatus.WATCHING:
            raise HTTPException(
                status_code=400, detail="Can only invalidate trades in watching status"
            )
        trade.status = TradeStatus.INVALIDATED
        await self.repo.update_trade(trade_id, trade)

    async def delete_trade(self, trade_id: str) -> None:
        return await self.repo.delete_trade(trade_id)

    async def _get_price_map(self, symbols: list[str]):
        quotes = await self.finnhub_service.get_stock_price_batch(symbols)
        return {quote.symbol: quote for quote in quotes}

    async def _get_profile_map(self, symbols: list[str]):
        profiles = await self.finnhub_service.get_company_profile_batch(symbols)
        return {profile.ticker: profile for profile in profiles}

    async def _enrich_single_trade(self, trade: Trade) -> TradeResponse:
        """Enrich a single trade with current market data."""
        if not trade.symbol:
            return TradeResponse.model_validate(trade)

        try:
            quote_task = self.finnhub_service.get_stock_price(trade.symbol)
            profile_task = self.finnhub_service.get_company_profile(trade.symbol)

            quote, profile = await asyncio.gather(
                quote_task, profile_task, return_exceptions=True
            )

            price_map = (
                {trade.symbol: quote} if not isinstance(quote, Exception) else {}
            )
            profile_map = (
                {trade.symbol: profile} if not isinstance(profile, Exception) else {}
            )

            enriched_data = self._enrich_trade(trade, price_map, profile_map)
            return TradeResponse.model_validate(enriched_data)

        except Exception as e:
            logging.warning(f"Failed to enrich trade {trade.id} with market data: {e}")
            return TradeResponse.model_validate(trade)

    def _build_watchlist_payload(self, trade: TradeCreate):
        scale_plans = self._build_plans(trade.scale_plans)

        payload = trade.model_dump(exclude_none=True)
        payload.update(
            {
                "status": TradeStatus.WATCHING,
                "scale_plans": scale_plans,
            }
        )
        return payload

    @staticmethod
    def _enrich_trade(
        trade: Trade,
        price_map: Dict[str, StockQuote],
        profile_map: Dict[str, CompanyProfile],
    ):
        trade_data = TradeResponse.model_validate(trade).model_dump()

        if trade.symbol:
            if quote := price_map.get(trade.symbol):
                trade_data.update(
                    {
                        "current_price": quote.current_price,
                        "price_change": quote.change,
                        "percent_change": quote.percent_change,
                        "open_price": quote.open_price,
                        "previous_close": quote.previous_close,
                    }
                )

            if profile := profile_map.get(trade.symbol):
                trade_data.update(
                    {
                        "country": profile.country,
                        "currency": profile.currency,
                        "exchange": profile.exchange,
                        "name": profile.name,
                        "industry": profile.finnhubIndustry,
                        "logo": profile.logo,
                        "cap": profile.marketCapitalization,
                    }
                )

        return trade_data

    @staticmethod
    def _build_annotations(dto: TradeCreate):
        annotations: list[Annotation] = []
        if dto.notes:
            annotations.extend(
                Annotation(content=n, annotation_type=AnnotationType.note)
                for n in dto.notes
            )

        if dto.catalysts:
            annotations.extend(
                Annotation(content=c, annotation_type=AnnotationType.catalyst)
                for c in dto.catalysts
            )

        return annotations

    def _build_plans(self, plans: list[ScalePlanCreate]):
        # Empty plans are allowed
        if not plans:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one entry plan is required.",
            )

        entry_plan = next((p for p in plans if p.plan_type == PlanType.ENTRY), None)
        self._validate_entry_plan(entry_plan)
        self._validate_target_plan(plans, entry_plan)
        return [ScalePlan(**p.model_dump()) for p in plans]

    @staticmethod
    def _validate_entry_plan(plan: ScalePlanCreate):
        if not plan or plan.plan_type != PlanType.ENTRY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one entry plan is required.",
            )
        if plan.qty <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entry plan qty must be greater than 0.",
            )
        if (plan.limit_price or 0) <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entry plan limit price must be greater than 0.",
            )

        # Validate stop price exists and relationship to limit price based on trade type
        stop_price = plan.stop_price or 0
        limit_price = plan.limit_price or 0

        if stop_price <= 0:  # Not sure if I want to enforce this
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entry plan stop price must be greater than 0.",
            )

        # For long trades: stop < limit (stop loss below entry)
        # For short trades: stop > limit (stop loss above entry)
        if plan.trade_type == TradeType.LONG and stop_price >= limit_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="For long trades, stop price must be less than limit price.",
            )
        elif plan.trade_type == TradeType.SHORT and stop_price <= limit_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="For short trades, stop price must be greater than limit price.",
            )

    @staticmethod
    def _validate_target_plan(
        plans: list[ScalePlanCreate], entry_plan: ScalePlanCreate
    ):
        target_plans = [p for p in plans if p.plan_type == PlanType.TARGET]

        # Allow at most one TARGET plan with no explicit target price (remainder)
        none_target_count = sum(
            1 for p in target_plans if getattr(p, "target_price", None) is None
        )
        if none_target_count > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At most one TARGET plan may have a null target_price (remainder).",
            )

        # Validate total target shares don't exceed entry shares
        if target_plans:
            total_target_qty = sum(p.qty for p in target_plans)
            if total_target_qty > entry_plan.qty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total target shares cannot exceed entry shares.",
                )
