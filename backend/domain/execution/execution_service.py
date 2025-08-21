from fastapi import HTTPException, status

from database.models import TradeExecution
from domain.execution.execution_repo import ExecutionRepo
from domain.execution.execution_schema import (
    ExecutionRead,
    ExecutionCreate,
    ExecutionUpdate,
)


class ExecutionService:
    def __init__(self, repo: ExecutionRepo):
        self.repo = repo

    async def get_executions(self, trade_id: str | None = None) -> list[TradeExecution]:
        return await self.repo.get_executions(trade_id)

    async def get_execution_by_id(self, execution_id: str) -> TradeExecution | None:
        return await self.repo.get_execution_by_id(execution_id)

    async def create_execution(self, payload: ExecutionCreate) -> TradeExecution:
        data = payload.model_dump()
        execution = TradeExecution(**data)
        return await self.repo.execute(execution)

    async def update_execution(
        self, execution_id: str, payload: ExecutionUpdate
    ) -> TradeExecution:
        return await self.repo.update_execution(execution_id, payload)

    async def delete_execution(self, execution_id: str) -> None:
        db_execution = await self.repo.get_execution_by_id(execution_id)
        if not db_execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Execution not found"
            )
        return await self.repo.delete_execution(execution_id)
