from typing import Annotated

from fastapi import Depends

from domain.scale_plan.scale_plan_repo import ScalePlanRepo
from database.session import SessionDep
from domain.scale_plan.scale_plan_service import ScalePlanService


def get_scale_plan_repo(session: SessionDep) -> ScalePlanRepo:
    return ScalePlanRepo(session=session)


def get_scale_plan_service(
    repo: ScalePlanRepo = Depends(get_scale_plan_repo),
) -> ScalePlanService:
    return ScalePlanService(repo=repo)


ScalePlanServiceDep = Annotated[ScalePlanService, Depends(get_scale_plan_service)]
