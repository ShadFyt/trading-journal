from fastapi import APIRouter, status
from typing import Optional

from domain.scale_plan.scale_plan_deps import ScalePlanServiceDep
from domain.scale_plan.scale_plan_schema import (
    ScalePlanRead,
    ScalePlanCreateWithTradeId,
)

router = APIRouter()


@router.get("", response_model=list[ScalePlanRead])
async def get_all_scale_plans_by_trade(
    service: ScalePlanServiceDep, trade_id: Optional[str] = None
):
    if trade_id:
        return await service.get_all_scale_plans_by_trade(trade_id)
    return await service.get_all_scale_plans()


@router.post("", response_model=ScalePlanRead)
async def create_scale_plan(
    service: ScalePlanServiceDep, scale_plan: ScalePlanCreateWithTradeId
):
    return await service.create_scale_plan(scale_plan)


@router.delete("/{scale_plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scale_plan(service: ScalePlanServiceDep, scale_plan_id: str):
    return await service.delete_scale_plan(scale_plan_id)
