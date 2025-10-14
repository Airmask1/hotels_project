from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/{room_id}")
async def create_booking(
    db: DBDep,
    room_id: int,
    user_id: UserIdDep,
    booking_data: BookingAdd = Body(),
):
    room = await db.rooms.get_one_or_none(room_id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    user = await db.users.get_one_or_none(id=user_id)
    room_price = room.price
    if user:
        booking = await db.bookings.add(
            booking_data, room_id=room_id, price=room_price, user_id=user_id
        )
        await db.commit()
        return {"status": "OK", "data": booking}
