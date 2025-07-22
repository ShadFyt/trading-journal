from fastapi import APIRouter
from domain.trade_idea.trade_idea_deps import TradeIdeaServiceDep
from domain.trade_idea.trade_idea_schema import TradeIdeaResponse, TradeIdeaCreate, TradeIdeaUpdate
from fastapi import status

router = APIRouter()

@router.get("", response_model=list[TradeIdeaResponse])
async def get_trade_ideas(service: TradeIdeaServiceDep):
    return await service.get_all_trade_ideas()

@router.post("", response_model=TradeIdeaResponse)
async def create_trade_idea(service: TradeIdeaServiceDep, trade_idea: TradeIdeaCreate):
    return await service.create_trade_idea(trade_idea)

@router.patch("/{id}", response_model=TradeIdeaResponse)
async def update_trade_idea(service: TradeIdeaServiceDep, id: str, payload: TradeIdeaUpdate):
    return await service.update_trade_idea(id, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade_idea(service: TradeIdeaServiceDep, id: str):
    return await service.delete_trade_idea(id)