from typing import TypeVar, Generic, List, Optional, Type
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
import asyncio

T = TypeVar("T", bound=SQLModel)

class BaseRepo(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
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

    async def _save(self, instance: T) -> T:
        """Save instance to database and refresh."""
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
