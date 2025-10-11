from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.repos.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


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
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):

    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(hotel_data, id=hotel_id)
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Hotel not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.post("")
async def create_hotel(
    hotel_data: HotelAdd = Body(
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
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).edit(hotel_data, id=hotel_id, patch=True)
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Hotel not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).delete(id=hotel_id)
            await session.commit()
            return {"status": "OK"}
        except ObjectNotFoundError:
            raise HTTPException(status_code=404, detail="Hotel not found")
        except MultipleObjectsFoundError:
            raise HTTPException(status_code=400, detail="Multiple objects were found")
