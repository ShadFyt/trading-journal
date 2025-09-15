from database.session import SessionDep
from domain.trade.trade_repo import TradeRepo
from fastapi import Depends
from domain.trade.trade_service import TradeService
from domain.annotation.annotation_deps import get_annotation_repo
from typing import Annotated
from domain.annotation.annotation_repo import AnnotationRepo
from core.stock_price.finnhub_service import FinnhubService


def get_stock_price_service() -> FinnhubService:
    return FinnhubService()


def get_trade_repo(session: SessionDep) -> TradeRepo:
    return TradeRepo(session=session)


def get_trade_service(
    repo: TradeRepo = Depends(get_trade_repo),
    annotation_repo: AnnotationRepo = Depends(get_annotation_repo),
    stock_price_service: FinnhubService = Depends(get_stock_price_service),
) -> TradeService:
    return TradeService(
        repo=repo,
        annotation_repo=annotation_repo,
        stock_price_service=stock_price_service,
    )


TradeServiceDep = Annotated[TradeService, Depends(get_trade_service)]
