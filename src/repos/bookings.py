from sqlalchemy import delete, insert, select, update

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.schemas.bookings import Booking, BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    def __init__(self, session):
        self.session = session

    # async def get_all(self, hotel_id: int):
    #     query = select(self.model)
    #     if hotel_id:
    #         query = query.where(self.model.hotel_id == hotel_id)
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model) for model in result.scalars().all()]

    # async def get_one_or_none(self, hotel_id: int, room_id: int):
    #     query = select(self.model)
    #     if hotel_id and room_id:
    #         query = query.where(
    #             self.model.hotel_id == hotel_id, self.model.id == room_id
    #         )
    #     result = await self.session.execute(query)
    #     model = result.scalars().one_or_none()
    #     return None if model is None else self.schema.model_validate(model)

    async def add(self, booking: BookingAdd, room_id: int, user_id: int, price: int):
        stmt = (
            insert(self.model)
            .values(
                **booking.model_dump(), room_id=room_id, user_id=user_id, price=price
            )
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        m = result.scalars().first()
        return self.schema.model_validate(m, from_attributes=True)
