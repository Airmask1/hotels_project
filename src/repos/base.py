from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.scalars(add_stmt)
        return result.first()

    async def edit(self, data: BaseModel, patch: bool = False, **filter_by) -> None:

        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=patch))
        )
        result = await self.session.execute(update_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundError("Object not found")
        if result.rowcount > 1:
            raise MultipleObjectsFoundError("Multiple objects were found")

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        if result.rowcount == 0:
            raise ObjectNotFoundError("Object not found")
        if result.rowcount > 1:
            raise MultipleObjectsFoundError("Multiple objects were found")
