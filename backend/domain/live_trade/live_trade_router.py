from fastapi import APIRouter
from domain.live_trade.live_trade_deps import LiveTradeServiceDep
from domain.live_trade.live_trade_schema import LiveTradeResponse, LiveTradeCreate, LiveTradeUpdate
from fastapi import status

router = APIRouter()

@router.get("", response_model=list[LiveTradeResponse])
async def get_live_trades(service: LiveTradeServiceDep):
    return await service.get_all_live_trades()

@router.post("", response_model=LiveTradeResponse , status_code=status.HTTP_201_CREATED)
async def create_live_trade(service: LiveTradeServiceDep, live_trade: LiveTradeCreate):
    return await service.create_live_trade(live_trade)

@router.patch("/{id}", response_model=LiveTradeResponse, status_code=status.HTTP_200_OK)
async def update_live_trade(service: LiveTradeServiceDep, id: str, payload: LiveTradeUpdate):
    return await service.update_live_trade(id, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_live_trade(service: LiveTradeServiceDep, id: str):
    return await service.delete_live_trade(id)
