from domain.trade.trade_repo import TradeRepo
from domain.trade.trade_schema import (
    TradeCreate,
    TradeUpdate,
    TradeResponse,
)
from domain.scale_plan.scale_plan_schema import ScalePlanCreate
from domain.trade_idea.trade_idea_service import TradeIdeaService
from domain.annotation.annotation_repo import AnnotationRepo
from database.models import (
    Annotation,
    Trade,
    AnnotationType,
    TradeStatus,
    ScalePlan,
)
from fastapi import HTTPException, status
from core.stock_price.stock_price_service import StockPriceService


class TradeService:
    def __init__(
        self,
        repo: TradeRepo,
        annotation_repo: AnnotationRepo,
        trade_idea_service: TradeIdeaService,
        stock_price_service: StockPriceService,
    ):
        self.repo = repo
        self.annotation_repo = annotation_repo
        self.trade_idea_service = trade_idea_service
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
            price_map = self._get_price_map(symbols)
            # Merge current price data with live trades
            for trade in trades:
                if trade.symbol in price_map:
                    quote = price_map[trade.symbol]
                    trade.current_price = quote.current_price
                    trade.price_change = quote.change
                    trade.percent_change = quote.percent_change
        except Exception as e:
            # Log error but don't fail the entire request
            print(f"Warning: Could not fetch current prices: {e}")

        return trades

    async def get_live_trade_by_id(self, live_trade_id: str) -> TradeResponse | None:
        return await self.repo.get_trade_by_id(live_trade_id)

    async def create_trade(self, trade: TradeCreate) -> TradeResponse:
        payload = self._build_payload(trade)
        # Create LiveTrade instance
        trade_instance = Trade(**payload)

        # Create the trade
        result = await self.repo.create_trade(trade_instance)

        return result

    async def update_trade(
        self, trade_id: str, payload: TradeUpdate
    ) -> TradeResponse | None:
        return await self.repo.update_trade(trade_id, payload)

    async def delete_trade(self, trade_id: str) -> None:
        return await self.repo.delete_trade(trade_id)

    def _get_price_map(self, symbols: list[str]):
        quotes = self.stock_price_service.get_stock_price_batch(symbols)
        return {quote.symbol: quote for quote in quotes}

    def _build_payload(self, trade: TradeCreate):
        annotations = self._build_annotations(trade)
        scale_plans = self._build_scale_plans(trade.scale_plans, trade.position_size)
        payload = trade.model_dump(exclude_none=True)
        payload.update(
            {
                "status": TradeStatus.WATCHING,
                "annotations": annotations,
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

    @staticmethod
    def _build_scale_plans(plans: list[ScalePlanCreate], position_size: int):
        # Empty plans are allowed
        if not plans:
            return []

        # Allow at most one 'remainder' plan with no explicit target price
        none_target_count = sum(
            1 for p in plans if getattr(p, "target_price", None) is None
        )
        if none_target_count > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At most one scale plan may have a null target_price (remainder).",
            )

        # Validate total shares don't exceed position size
        total_qty = sum(p.qty for p in plans)
        if total_qty > position_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total shares for scale plans cannot exceed position size.",
            )

        return [ScalePlan(**p.model_dump()) for p in plans]
