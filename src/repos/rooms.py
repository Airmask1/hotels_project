from datetime import date

from sqlalchemy import func, insert, select

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.utils import rooms_ids_for_bookings
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    def __init__(self, session):
        self.session = session

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        vacant_rooms_ids = rooms_ids_for_bookings(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return await self.get_filtered(self.model.id.in_(vacant_rooms_ids))

    async def get_one_or_none(self, room_id: int, hotel_id: int | None = None):
        query = select(self.model).filter(self.model.id == room_id)
        if hotel_id:
            query = query.filter(self.model.hotel_id == hotel_id)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return None if model is None else self.schema.model_validate(model)

    async def add(self, room: RoomAdd, hotel_id: int):
        stmt = (
            insert(self.model)
            .values(**room.model_dump(), hotel_id=hotel_id)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        m = result.scalars().first()
        return self.schema.model_validate(m, from_attributes=True)
