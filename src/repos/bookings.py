from sqlalchemy import delete, insert, select, update

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingDataMapper
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    def __init__(self, session):
        self.session = session

    async def user_bookings(self, user_id: int):
        query = select(self.model)
        if user_id:
            query = query.where(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def add(self, booking: BookingAdd, user_id: int, price: int):
        stmt = (
            insert(self.model)
            .values(**booking.model_dump(), user_id=user_id, price=price)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        m = result.scalars().first()
        return self.mapper.map_to_domain_entity(m)
