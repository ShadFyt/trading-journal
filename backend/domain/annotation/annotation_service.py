from domain.annotation.annotation_repo import AnnotationRepo
from domain.annotation.annotation_schema import AnnotationCreate, AnnotationUpdate
from typing import Literal

class AnnotationService:
    def __init__(self, repo: AnnotationRepo):
        self.repo = repo
    
    def create_annotation(self, annotationDto: AnnotationCreate):
        return self.repo.create_annotation(annotationDto)
    
    def get_annotation_by_id(self, id: str):
        return self.repo.get_annotation_by_id(id)
    
    def get_all_annotations(self, type_filter: Literal['catalyst', 'note', 'managementNote'] | None = None):
        return self.repo.get_all_annotations(type_filter)
    
    def update_annotation(self, id: str, payload: AnnotationUpdate):
        return self.repo.update_annotation(id, payload)
    
    def delete_annotation(self, id: str):
        return self.repo.delete_annotation(id)