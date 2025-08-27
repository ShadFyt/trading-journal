from fastapi import HTTPException, status

from database.models import TradeExecution, ScalePlan, ScalePlanStatus
from domain.execution.execution_repo import ExecutionRepo
from domain.scale_plan.scale_plan_repo import ScalePlanRepo
from domain.execution.execution_schema import (
    ExecutionRead,
    ExecutionCreate,
    ExecutionUpdate,
)


class ExecutionService:
    def __init__(self, repo: ExecutionRepo, scale_plan_repo: ScalePlanRepo = None):
        self.repo = repo
        self.scale_plan_repo = scale_plan_repo

    async def get_executions(self, trade_id: str | None = None) -> list[TradeExecution]:
        return await self.repo.get_executions(trade_id)

    async def get_execution_by_id(self, execution_id: str) -> TradeExecution | None:
        return await self.repo.get_execution_by_id(execution_id)

    async def create_execution(self, payload: ExecutionCreate) -> TradeExecution:
        data = payload.model_dump()
        execution = TradeExecution(**data)
        
        # Create the execution first
        created_execution = await self.repo.execute(execution)
        
        # Update scale plan status if execution is linked to a scale plan
        if created_execution.scale_plan_id and self.scale_plan_repo:
            await self._update_scale_plan_status(created_execution)
        
        return created_execution

    async def _update_scale_plan_status(self, execution: TradeExecution) -> None:
        """Update scale plan status based on execution."""
        if not execution.scale_plan_id:
            return
            
        scale_plan = await self.scale_plan_repo.get_scale_plan_by_id(execution.scale_plan_id)
        if not scale_plan:
            return
            
        # Calculate total executed quantity for this scale plan
        total_executed_qty = sum(exec.qty for exec in scale_plan.executions)
        
        # Determine new status based on execution logic
        if scale_plan.kind == "shares":
            target_qty = scale_plan.value
        else:  # percent
            # You'll need the live trade to calculate percent-based quantities
            # This assumes you have access to the live trade through relationships
            if hasattr(scale_plan, 'live_trade') and scale_plan.live_trade:
                target_qty = int(scale_plan.live_trade.position_size * (scale_plan.value / 100))
            else:
                return  # Can't calculate without live trade info
        
        # Update status based on execution progress
        new_status = scale_plan.status
        if total_executed_qty >= target_qty:
            new_status = ScalePlanStatus.FILLED
        elif total_executed_qty > 0:
            new_status = ScalePlanStatus.FILLED_PARTIAL
        elif scale_plan.status == ScalePlanStatus.PLANNED:
            new_status = ScalePlanStatus.TRIGGERED
            
        # Only update if status changed
        if new_status != scale_plan.status:
            from domain.scale_plan.scale_plan_schema import ScalePlanUpdate
            update_payload = ScalePlanUpdate(status=new_status)
            await self.scale_plan_repo.update_by_id(scale_plan.id, update_payload)

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
