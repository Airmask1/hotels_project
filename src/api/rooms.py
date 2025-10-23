from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("")
async def get_hotel_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):

    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{room_id}")
async def get_hotel_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, room_id=room_id)


@router.put("/{room_id}")
async def put_hotel_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAdd):

    try:
        await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ObjectNotFoundError:
        raise HTTPException(status_code=404, detail="Room not found")
    except MultipleObjectsFoundError:
        raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.post("")
async def create_hotel_room(
    db: DBDep,
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

    room = await db.rooms.add(room_data, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK", "data": room}


@router.patch("/{room_id}")
async def patch_hotel_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatch
):
    try:
        await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id, patch=True)
        await db.commit()
        return {"status": "OK"}
    except ObjectNotFoundError:
        raise HTTPException(status_code=404, detail="Room not found")
    except MultipleObjectsFoundError:
        raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.delete("/{room_id}")
async def delete_hotel_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()
        return {"status": "OK"}
    except ObjectNotFoundError:
        raise HTTPException(status_code=404, detail="Hotel not found")
    except MultipleObjectsFoundError:
        raise HTTPException(status_code=400, detail="Multiple objects were found")
