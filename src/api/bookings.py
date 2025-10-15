from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAdd = Body(),
):
    room = await db.rooms.get_one_or_none(room_id=booking_data.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    user = await db.users.get_one_or_none(id=user_id)
    room_price = room.price
    if user:
        booking = await db.bookings.add(booking_data, price=room_price, user_id=user_id)
        await db.commit()
        return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.user_bookings(user_id=user_id)
