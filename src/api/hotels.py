from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repos.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    location: Optional[str] = Query(None, description="Hotel address"),
    title: Optional[str] = Query(
        None, min_length=3, max_length=100, description="Hotel name"
    ),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.get("/{hotel_id}")
def get_hotel_by_id(hotel_id: int):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel
    raise HTTPException(status_code=404, detail="Hotel not found")


@router.put("/{hotel_id}")
def put_hotel(
    hotel_id: int, name: str = Body(), address: str = Body(), rooms: int = Body()
):
    global hotels
    new_hotel = {"id": hotel_id, "name": name, "address": address, "rooms": rooms}
    for h in hotels:
        if h.get("id") == hotel_id:
            h.update(new_hotel)
            return h

    raise HTTPException(status_code=404, detail="Hotel not found")


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {
                    "title": "Deluxe 5",
                    "location": "Sochi, Gor'kogo 127",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "White Night",
                    "location": "Dubai, Arid 120",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    for h in hotels:
        if h.get("id") == hotel_id:
            if hotel_data.name:
                h["name"] = hotel_data.name
            if hotel_data.address:
                h["address"] = hotel_data.address
            if hotel_data.rooms:
                h["rooms"] = hotel_data.rooms
            return h

    raise HTTPException(status_code=404, detail="Hotel not found")
