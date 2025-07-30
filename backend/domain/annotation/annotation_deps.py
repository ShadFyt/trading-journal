from domain.annotation.annotation_repo import AnnotationRepo
from database.session import SessionDep

def get_annotation_repo(session: SessionDep) -> AnnotationRepo:
    return AnnotationRepo(session=session)
