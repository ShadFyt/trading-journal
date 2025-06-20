from typing import Annotated

from database.session import SessionDep
from domain.trade_idea.trade_idea_repo import TradeIdeaRepo
from domain.trade_idea.trade_idea_service import TradeIdeaService
from fastapi import Depends


def get_trade_idea_repo(session: SessionDep) -> TradeIdeaRepo:
    return TradeIdeaRepo(session=session)


def get_trade_idea_service(
    repo: TradeIdeaRepo = Depends(get_trade_idea_repo),
) -> TradeIdeaService:
    return TradeIdeaService(repo=repo)


TradeIdeaServiceDep = Annotated[TradeIdeaService, Depends(get_trade_idea_service)]
