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
from core.stock_price.stock_price_service import StockPriceService


class TradeService:
    def __init__(
        self,
        repo: TradeRepo,
        annotation_repo: AnnotationRepo,
        stock_price_service: StockPriceService,
    ):
        self.repo = repo
        self.annotation_repo = annotation_repo
        self.stock_price_service = stock_price_service

    async def get_all_trades(self) -> list[TradeResponse]:
        # Get all trades from the repository
        db_trades = await self.repo.get_all_trades()

        # Convert SQLModel instances to Pydantic models for modification
        trades = [TradeResponse.model_validate(trade) for trade in db_trades]

        # Extract unique symbols from live trades
        symbols = list(dict.fromkeys(t.symbol for t in trades if t.symbol))
        if not symbols:
            return trades

        # Fetch current prices for all symbols
        try:
            price_map = await self._get_price_map(symbols)
            # Merge current price data with live trades
            for trade in trades:
                if trade.symbol in price_map:
                    quote = price_map[trade.symbol]
                    trade.current_price = quote.current_price
                    trade.price_change = quote.change
                    trade.percent_change = quote.percent_change
                    trade.open_price = quote.open_price
                    trade.previous_close = quote.previous_close
        except Exception as e:
            # Log error but don't fail the entire request
            print(f"Warning: Could not fetch current prices: {e}")

        return trades

    async def get_live_trade_by_id(self, live_trade_id: str) -> TradeResponse | None:
        return await self.repo.get_trade_by_id(live_trade_id)

    async def create_trade(self, trade: TradeCreate) -> TradeResponse:
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

    async def replace_trade(self, trade_id: str, payload: TradeCreate) -> Trade:
        """Replace an existing trade with new data while preserving certain fields."""
        # Convert TradeCreate to TradeUpdate for the repository method
        # TradeUpdate should have all the same fields as TradeCreate but as optional
        trade_update_data = payload.model_dump()
        trade_update = TradeUpdate(**trade_update_data)

        # Replace the trade in the repository using SQLModel patterns
        result = await self.repo.replace_trade(trade_id, trade_update)

        return result

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
        quotes = await self.stock_price_service.get_stock_price_batch(symbols)
        return {quote.symbol: quote for quote in quotes}

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
