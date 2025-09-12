from fastapi import APIRouter
from domain.trade.trade_deps import TradeServiceDep
from domain.trade.trade_schema import (
    TradeResponse,
    TradeCreate,
    TradeUpdate,
)
from fastapi import status

router = APIRouter()


@router.get("", response_model=list[TradeResponse])
async def get_live_trades(service: TradeServiceDep):
    return await service.get_all_trades()


@router.post("", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
async def create_live_trade(service: TradeServiceDep, live_trade: TradeCreate):
    return await service.create_trade(live_trade)


@router.put("/{trade_id}", response_model=TradeResponse, status_code=status.HTTP_200_OK)
async def replace_trade(service: TradeServiceDep, trade_id: str, payload: TradeCreate):
    return await service.replace_trade(trade_id, payload)


@router.patch("/{id}", response_model=TradeResponse, status_code=status.HTTP_200_OK)
async def update_live_trade(service: TradeServiceDep, id: str, payload: TradeUpdate):
    return await service.update_trade(id, payload)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_live_trade(service: TradeServiceDep, id: str):
    return await service.delete_trade(id)
