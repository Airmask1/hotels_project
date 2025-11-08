from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundError
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.repos.rooms import RoomsOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def edit(
        self,
        facilities_ids,
        room_id,
    ):
        query = (
            select(RoomsOrm)
            .where(RoomsOrm.id == room_id)
            .options(selectinload(RoomsOrm.facilities))
        )
        result = await self.session.execute(query)
        room = result.scalar_one_or_none()
        if not room:
            return ObjectNotFoundError("Room with id {room_id} not found.")

        facilities_query = select(FacilitiesOrm).where(
            FacilitiesOrm.id.in_(facilities_ids)
        )
        facilities_result = await self.session.execute(facilities_query)
        new_facilities = facilities_result.scalars().all()

        room.facilities = new_facilities
