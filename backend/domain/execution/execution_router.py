from fastapi import APIRouter, status
from typing import Optional

from domain.execution.execution_deps import ExecutionServiceDep
from domain.execution.execution_schema import (
    ExecutionRead,
    ExecutionCreate,
    ExecutionUpdate,
)

router = APIRouter()


@router.get("", response_model=list[ExecutionRead], status_code=status.HTTP_200_OK)
async def get_executions(service: ExecutionServiceDep, trade_id: Optional[str] = None):
    return await service.get_executions(trade_id)


@router.get(
    "/{execution_id}", response_model=ExecutionRead, status_code=status.HTTP_200_OK
)
async def get_execution_by_id(service: ExecutionServiceDep, execution_id: str):
    return await service.get_execution_by_id(execution_id)


@router.post("", response_model=ExecutionRead, status_code=status.HTTP_201_CREATED)
async def create_execution(service: ExecutionServiceDep, payload: ExecutionCreate):
    return await service.create_execution(payload)


@router.patch(
    "/{execution_id}", response_model=ExecutionRead, status_code=status.HTTP_200_OK
)
async def update_execution(
    service: ExecutionServiceDep, execution_id: str, payload: ExecutionUpdate
):
    return await service.update_execution(execution_id, payload)


@router.delete("/{execution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_execution(service: ExecutionServiceDep, execution_id: str):
    return await service.delete_execution(execution_id)
