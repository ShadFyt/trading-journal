from database.session import SessionDep
from domain.live_trade.live_trade_repo import LiveTradeRepo
from fastapi import Depends
from domain.live_trade.live_trade_service import LiveTradeService
from typing import Annotated

def get_live_trade_repo(session: SessionDep) -> LiveTradeRepo:
    return LiveTradeRepo(session=session)

def get_live_trade_service(
    repo: LiveTradeRepo = Depends(get_live_trade_repo),
) -> LiveTradeService:
    return LiveTradeService(repo=repo)

LiveTradeServiceDep = Annotated[LiveTradeService, Depends(get_live_trade_service)]