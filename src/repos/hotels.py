from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.base import DataMapper
from src.repos.mappers.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_bookings


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper: DataMapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str,
        title: str,
        limit: int,
        offset: int,
    ):
        vacant_rooms_ids = rooms_ids_for_bookings(date_from=date_from, date_to=date_to)
        hotels_ids = select(RoomsOrm.hotel_id).filter(RoomsOrm.id.in_(vacant_rooms_ids))
        query = select(self.model)
        if location:
            query = query.filter(self.model.location.like(f"%{location.strip()}%"))
        if title:
            query = query.filter(self.model.title.ilike(f"%{title.strip()}%"))
        query = query.filter(self.model.id.in_(hotels_ids))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]
