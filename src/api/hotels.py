from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep, PaginationParams
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        query = query.limit(per_page).offset(per_page * (pagination.page - 1))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
                    "title": "Hotel in Sochi with 5 starts",
                    "location": "sochi_127",
                },
            },
            "2": {
                "summary": "Dubai",
                "value": {
                    "title": "Abu-Dabi-Hotel",
                    "location": "sheich_150",
                },
            },
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


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
