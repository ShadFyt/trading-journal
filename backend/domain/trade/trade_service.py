from domain.trade.trade_repo import LiveTradeRepo
from domain.trade.trade_schema import (
    LiveTradeCreate,
    LiveTradeUpdate,
    LiveTradeResponse,
)
from domain.scale_plan.scale_plan_schema import ScalePlanCreate
from domain.trade_idea.trade_idea_schema import TradeIdeaUpdate
from domain.trade_idea.trade_idea_service import TradeIdeaService
from domain.annotation.annotation_repo import AnnotationRepo
from database.models import (
    Annotation,
    Trade,
    TradeIdeaStatus,
    AnnotationType,
    LiveTradeStatus,
    ScalePlan,
    ScalePlanKind,
)
from fastapi import HTTPException, status
from core.stock_price.stock_price_service import StockPriceService


class LiveTradeService:
    def __init__(
        self,
        repo: LiveTradeRepo,
        annotation_repo: AnnotationRepo,
        trade_idea_service: TradeIdeaService,
        stock_price_service: StockPriceService,
    ):
        self.repo = repo
        self.annotation_repo = annotation_repo
        self.trade_idea_service = trade_idea_service
        self.stock_price_service = stock_price_service

    async def get_all_live_trades(self) -> list[LiveTradeResponse]:
        # Get all live trades from the repository
        db_live_trades = await self.repo.get_all_live_trades()

        # Convert SQLModel instances to Pydantic models for modification
        live_trades = [
            LiveTradeResponse.model_validate(trade) for trade in db_live_trades
        ]

        # Extract unique symbols from live trades
        symbols = list(dict.fromkeys(t.symbol for t in live_trades if t.symbol))
        if not symbols:
            return live_trades

        # Fetch current prices for all symbols
        try:
            price_map = self._get_price_map(symbols)
            # Merge current price data with live trades
            for trade in live_trades:
                if trade.symbol in price_map:
                    quote = price_map[trade.symbol]
                    trade.current_price = quote.current_price
                    trade.price_change = quote.change
                    trade.percent_change = quote.percent_change
        except Exception as e:
            # Log error but don't fail the entire request
            print(f"Warning: Could not fetch current prices: {e}")

        return live_trades

    async def get_live_trade_by_id(
        self, live_trade_id: str
    ) -> LiveTradeResponse | None:
        return await self.repo.get_live_trade_by_id(live_trade_id)

    async def create_live_trade(self, live_trade: LiveTradeCreate) -> LiveTradeResponse:
        if await self.repo.get_live_trade_by_trade_idea_id(live_trade.trade_idea_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Live trade already exists for this trade idea",
            )

        payload = self._build_payload(live_trade)
        # Create LiveTrade instance
        live_trade_instance = Trade(**payload)

        # Create the live trade
        result = await self.repo.create_live_trade(live_trade_instance)

        # Update the associated TradeIdea status to Live
        await self.trade_idea_service.update_trade_idea(
            live_trade.trade_idea_id, TradeIdeaUpdate(status=TradeIdeaStatus.LIVE)
        )

        return result

    async def update_live_trade(
        self, live_trade_id: str, payload: LiveTradeUpdate
    ) -> LiveTradeResponse | None:
        return await self.repo.update_live_trade(live_trade_id, payload)

    async def delete_live_trade(self, live_trade_id: str) -> None:
        return await self.repo.delete_live_trade(live_trade_id)

    def _get_price_map(self, symbols: list[str]):
        quotes = self.stock_price_service.get_stock_price_batch(symbols)
        return {quote.symbol: quote for quote in quotes}

    def _build_payload(self, live_trade: LiveTradeCreate):
        annotations = self._build_annotations(live_trade)
        scale_plans = self._build_scale_plans(
            live_trade.scale_plans, live_trade.position_size
        )
        payload = live_trade.model_dump(
            exclude={"notes", "catalysts"}, exclude_none=True
        )
        payload.update(
            {
                "status": LiveTradeStatus.OPEN,
                "commissions": payload.get("commissions", 2),
                "annotations": annotations,
                "scale_plans": scale_plans,
            }
        )
        return payload

    @staticmethod
    def _build_annotations(dto: LiveTradeCreate):
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

    @staticmethod
    def _build_scale_plans(plans: list[ScalePlanCreate], position_size: int):
        # Empty plans are allowed
        if not plans:
            return []

        # Ensure all plans use the same kind
        kinds = {p.kind for p in plans}
        if len(kinds) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All scale plans must use the same kind.",
            )

        kind = next(iter(kinds))

        # Allow at most one 'remainder' plan with no explicit target price
        none_target_count = sum(
            1 for p in plans if getattr(p, "target_price", None) is None
        )
        if none_target_count > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At most one scale plan may have a null target_price (remainder).",
            )
        total_value = sum(p.value for p in plans)

        if kind == ScalePlanKind.PERCENT:
            # Combined percent cannot exceed 100
            if total_value > 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total percent for scale plans cannot exceed 100.",
                )
        else:
            # Assume shares; combined shares cannot exceed position size
            if total_value > position_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Total shares for scale plans cannot exceed position size.",
                )

        return [ScalePlan(**p.model_dump()) for p in plans]
