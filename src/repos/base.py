from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.scalars(add_stmt)
        model = result.first()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, patch: bool = False, **filter_by) -> None:

        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=patch))
        )
        model = await self.session.execute(update_stmt)
        if model.rowcount == 0:
            raise ObjectNotFoundError("Object not found")
        if model.rowcount > 1:
            raise MultipleObjectsFoundError("Multiple objects were found")

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        model = await self.session.execute(delete_stmt)
        if model.rowcount == 0:
            raise ObjectNotFoundError("Object not found")
        if model.rowcount > 1:
            raise MultipleObjectsFoundError("Multiple objects were found")
