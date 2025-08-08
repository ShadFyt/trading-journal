from fastapi import APIRouter
from domain.annotation.annotation_deps import AnnotationServiceDep
from domain.annotation.annotation_schema import AnnotationCreate, AnnotationRead
from fastapi import status

router = APIRouter()



@router.post("", response_model=AnnotationRead, status_code=status.HTTP_201_CREATED)
async def create_annotation(service: AnnotationServiceDep, annotationDto: AnnotationCreate):
    return await service.create_annotation(annotationDto)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(service: AnnotationServiceDep, id: str):
    return await service.delete_annotation(id)
