from typing import Annotated, Optional

from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.repos.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("")
async def get_hotel_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{room_id}")
async def get_hotel_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id, room_id=room_id
        )


@router.put("/{room_id}")
async def put_hotel_room(hotel_id: int, room_id: int, room_data: RoomAdd):

    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).edit(
                room_data, id=room_id, hotel_id=hotel_id
            )
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Room not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.post("")
async def create_hotel_room(
    hotel_id: int,
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Five Luxe hotel room",
                "value": {
                    "title": "Mountain View Cabin",
                    "description": "Wooden cabin with fireplace and stunning mountain view.",
                    "price": 190,
                    "quantity": 4,
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Garden Twin Room",
                    "description": "Overlooks garden, includes balcony and tea/coffee set.",
                    "price": 100,
                    "quantity": 5,
                },
            },
        }
    ),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {"status": "OK", "data": room}


@router.patch("/{room_id}")
async def patch_hotel_room(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).edit(
                room_data, id=room_id, hotel_id=hotel_id, patch=True
            )
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Room not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.delete("/{room_id}")
async def delete_hotel_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Hotel not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")
