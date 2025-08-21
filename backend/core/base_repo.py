from typing import TypeVar, Generic, List, Optional, Type
from sqlmodel import SQLModel, select
from database.session import SessionDep
from fastapi import HTTPException, status
import asyncio

T = TypeVar("T", bound=SQLModel)

class BaseRepo(Generic[T]):
    def __init__(self, session: SessionDep, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self, order_by=None) -> List[T]:
        try:
            stmt = select(self.model)
            if order_by is not None:
                stmt = stmt.order_by(order_by)
            results = await self.session.exec(stmt)
            return results.all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_by_id(self, id: str) -> Optional[T]:
        try:
            result = await self.session.get(self.model, id)
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.model.__name__} not found")
            return result
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def create(self, instance: T) -> T:
        try:
            # If instance is already a SQLModel object, use it directly
            # Otherwise, validate and create from raw data
            validated_instance= None
            if isinstance(instance, self.model):
                validated_instance = instance
            else:
                validated_instance = self.model.model_validate(instance)
            return await self._save(validated_instance)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete(self, id: str) -> None:
        try:
            found_instance = await self.get_by_id(id)
            await asyncio.shield(self.session.delete(found_instance))
            await asyncio.shield(self.session.commit())
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def update(self, id: str, payload) -> T:
        """Generic partial update by id.
        Accepts a Pydantic/SQLModel object or a plain dict. Only provided fields are updated.
        """
        try:
            instance = await self.get_by_id(id)
            # Normalize payload to a dict of changes (exclude fields not set)
            if isinstance(payload, SQLModel):
                data = payload.model_dump(exclude_unset=True)
            elif hasattr(payload, "model_dump"):
                data = payload.model_dump(exclude_unset=True)  # Pydantic v2 models
            elif isinstance(payload, dict):
                data = payload
            else:
                # Best effort: try SQLModel/Pydantic validation to the target model then dump
                tmp = self.model.model_validate(payload)
                data = tmp.model_dump(exclude_unset=True)

            # Prevent updating primary key
            data.pop("id", None)

            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            await asyncio.shield(self.session.commit())
            await asyncio.shield(self.session.refresh(instance))
            return instance
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def _save(self, instance: T) -> T:
        """Save instance to database and refresh."""
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
