from datetime import date

from sqlalchemy import delete, func, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def edit(self, facilities_ids, room_id, patch=False, **filter_by):
        existed_ids = await self.get_room_facilities(room_id=room_id)
        to_add_ids = set([f_id for f_id in facilities_ids if f_id not in existed_ids])
        to_delete_ids = set(existed_ids) - set(facilities_ids)
        await self.delete_batch(facility_ids=to_delete_ids)
        await self.add_batch(facility_ids=to_add_ids, room_id=room_id)

    async def get_room_facilities(self, room_id):
        query = select(self.model.facility_id).filter(self.model.room_id == room_id)
        result = await self.session.execute(query)
        rows = result.scalars().all()
        return rows

    async def delete_batch(
        self,
        facility_ids: list[int] | None = None,
    ) -> int:

        if not facility_ids:
            return ValueError("Delete batch needs facility_ids")

        stmt = delete(self.model)
        stmt = stmt.where(self.model.facility_id.in_(facility_ids))
        await self.session.execute(stmt)

    async def add_batch(self, room_id: int, facility_ids: list[int]) -> int:
        if not facility_ids:
            return 0

        rows = [{"room_id": room_id, "facility_id": f_id} for f_id in facility_ids]
        add_stmt = insert(self.model).values(rows)
        await self.session.execute(add_stmt)
