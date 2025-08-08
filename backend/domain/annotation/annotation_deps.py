from domain.annotation.annotation_repo import AnnotationRepo
from database.session import SessionDep
from domain.annotation.annotation_service import AnnotationService
from fastapi import Depends
from typing import Annotated

def get_annotation_repo(session: SessionDep) -> AnnotationRepo:
    return AnnotationRepo(session=session)


def get_annotation_service(repo: AnnotationRepo = Depends(get_annotation_repo)) -> AnnotationService:
    return AnnotationService(repo=repo)

AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]