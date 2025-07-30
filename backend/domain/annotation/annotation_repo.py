from database.session import SessionDep
from database.models import Annotation
from core.base_repo import BaseRepo
from domain.annotation.annotation_schema import AnnotationUpdate
from typing import Literal
from sqlmodel import select

class AnnotationRepo(BaseRepo[Annotation]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Annotation)
    
    async def get_all_annotations(self, type_filter: Literal['catalyst', 'note', 'managementNote'] | None = None):
        stmt = select(self.model)
        if type_filter:
            stmt = stmt.where(self.model.type == type_filter)
        results = await self.session.exec(stmt)
        return results.all()
    
    async def get_annotation_by_id(self, id: str):
        return await self.get_by_id(id)
    
    async def create_annotation(self, annotation: Annotation):
        return await self.create(annotation)
    
    async def update_annotation(self, id: str, payload: AnnotationUpdate):
        return await self.update(id, payload)
    
    async def delete_annotation(self, id: str):
        return await self.delete(id)