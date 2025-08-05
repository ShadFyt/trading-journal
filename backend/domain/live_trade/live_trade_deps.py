from database.session import SessionDep
from domain.live_trade.live_trade_repo import LiveTradeRepo
from domain.trade_idea.trade_idea_deps import get_trade_idea_service
from fastapi import Depends
from domain.live_trade.live_trade_service import LiveTradeService
from domain.trade_idea.trade_idea_service import TradeIdeaService
from domain.annotation.annotation_deps import get_annotation_repo
from typing import Annotated
from domain.annotation.annotation_repo import AnnotationRepo
from core.stock_price.stock_price_service import StockPriceService

def get_stock_price_service() -> StockPriceService:
    return StockPriceService()

def get_live_trade_repo(session: SessionDep) -> LiveTradeRepo:
    return LiveTradeRepo(session=session)

def get_live_trade_service(
    repo: LiveTradeRepo = Depends(get_live_trade_repo),
    annotation_repo: AnnotationRepo = Depends(get_annotation_repo),
    trade_idea_service: TradeIdeaService = Depends(get_trade_idea_service),
    stock_price_service: StockPriceService = Depends(get_stock_price_service),
) -> LiveTradeService:
    return LiveTradeService(repo=repo, trade_idea_service=trade_idea_service, annotation_repo=annotation_repo, stock_price_service=stock_price_service)

LiveTradeServiceDep = Annotated[LiveTradeService, Depends(get_live_trade_service)]