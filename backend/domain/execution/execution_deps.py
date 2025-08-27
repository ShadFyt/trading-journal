from fastapi import Depends
from typing import Annotated
from database.session import SessionDep
from domain.execution.execution_repo import ExecutionRepo
from domain.execution.execution_service import ExecutionService
from domain.scale_plan.scale_plan_repo import ScalePlanRepo


def get_execution_repo(session: SessionDep) -> ExecutionRepo:
    return ExecutionRepo(session=session)


def get_scale_plan_repo(session: SessionDep) -> ScalePlanRepo:
    return ScalePlanRepo(session=session)


def get_execution_service(
    repo: ExecutionRepo = Depends(get_execution_repo),
    scale_plan_repo: ScalePlanRepo = Depends(get_scale_plan_repo),
) -> ExecutionService:
    return ExecutionService(repo=repo, scale_plan_repo=scale_plan_repo)


ExecutionServiceDep = Annotated[ExecutionService, Depends(get_execution_service)]
