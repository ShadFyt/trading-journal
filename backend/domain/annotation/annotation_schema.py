from datetime import datetime
from typing import Optional
from core.base_schema import BaseSchema
from typing import Literal


class AnnotationBase(BaseSchema):
    content: str
    annotation_type: Literal["catalyst", "note", "managementNote"]


class AnnotationCreate(AnnotationBase):
    trade_id: str


class AnnotationRead(AnnotationCreate):
    id: str
    date: datetime


class AnnotationUpdate(AnnotationBase):
    annotation_type: Optional[Literal["catalyst", "note", "managementNote"]] = None
    content: Optional[str] = None
    date: Optional[datetime] = None
