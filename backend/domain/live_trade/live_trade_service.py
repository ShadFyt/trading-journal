import re
from domain.live_trade.live_trade_repo import LiveTradeRepo
from domain.live_trade.live_trade_schema import (
    LiveTradeCreate,
    LiveTradeUpdate,
    LiveTradeResponse,
)
from domain.trade_idea.trade_idea_service import TradeIdeaService
from domain.annotation.annotation_repo import AnnotationRepo
from database.models import Annotation, LiveTrade, TradeIdeaStatus
from datetime import datetime
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
        symbols = list(set(trade.symbol for trade in live_trades))

        # Fetch current prices for all symbols
        try:
            current_prices = self.stock_price_service.get_stock_price_batch(symbols)

            # Create a mapping of symbol to current price data
            price_map = {quote.symbol: quote for quote in current_prices}

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
        data = live_trade.model_dump()
        existing = await self.repo.get_live_trade_by_trade_idea_id(
            live_trade.trade_idea_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Live trade already exists for this trade idea",
            )

        data["status"] = "open"
        data["commissions"] = 2
        data["annotations"] = []

        if data["notes"]:
            note = Annotation(content=data["notes"][0], type="note")
            data["annotations"].append(note)

        if data["catalysts"]:
            catalyst = Annotation(
                content=data["catalysts"][0],
                type="catalyst",
            )
            data["annotations"].append(catalyst)

        # Create LiveTrade instance
        live_trade_instance = LiveTrade(**data)

        # Create the live trade
        result = await self.repo.create_live_trade(live_trade_instance)

        # Update the associated TradeIdea status to Live
        if live_trade.trade_idea_id:
            from domain.trade_idea.trade_idea_schema import TradeIdeaUpdate

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
