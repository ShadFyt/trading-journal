from fastapi import Depends
from typing import Annotated
from database.session import SessionDep
from domain.execution.execution_repo import ExecutionRepo
from domain.execution.execution_service import ExecutionService


def get_execution_repo(session: SessionDep) -> ExecutionRepo:
    return ExecutionRepo(session=session)


def get_execution_service(
    repo: ExecutionRepo = Depends(get_execution_repo),
) -> ExecutionService:
    return ExecutionService(repo=repo)


ExecutionServiceDep = Annotated[ExecutionService, Depends(get_execution_service)]
