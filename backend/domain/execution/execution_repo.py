from database.session import SessionDep
from database.models import TradeExecution
from core.base_repo import BaseRepo
from sqlmodel import select


class ExecutionRepo(BaseRepo):
    def __init__(self, session: SessionDep):
        super().__init__(session, TradeExecution)

    async def get_executions(self, trade_id: str | None = None) -> list[TradeExecution]:
        """
        Retrieve a list of all executions, ordered by executed_at.

        If trade_id is not None, only executions for the given trade are returned.
        """
        stmt = select(TradeExecution).order_by(TradeExecution.executed_at)
        if trade_id is not None:
            stmt = stmt.where(TradeExecution.trade_id == trade_id)
        result = await self.session.exec(stmt)
        return result.all()

    async def get_execution_by_id(self, execution_id: str) -> TradeExecution | None:
        return await self.get_by_id(execution_id)

    async def execute(self, execution: TradeExecution) -> TradeExecution:
        return await self.create(execution)

    async def update_execution(self, execution_id: str, execution: TradeExecution):
        return await self.update(execution_id, execution)

    async def delete_execution(self, execution_id: str):
        return await self.delete(execution_id)
