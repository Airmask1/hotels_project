from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if location:
            query = query.filter(self.model.location.like(f"%{location.strip()}%"))
        if title:
            query = query.filter(self.model.title.ilike(f"%{title.strip()}%"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]
