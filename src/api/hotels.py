from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from src.api.dependencies import PaginationDep, PaginationParams
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels")

hotels = [
    {
        "id": 1,
        "name": "Seaside Inn",
        "address": "123 Ocean Drive, Beach City",
        "rooms": 42,
    },
    {
        "id": 2,
        "name": "Mountain Lodge",
        "address": "77 Alpine Way, Hilltown",
        "rooms": 28,
    },
    {
        "id": 3,
        "name": "City Center Hotel",
        "address": "9 Central Plaza, Metropolis",
        "rooms": 120,
    },
    {
        "id": 4,
        "name": "Desert Oasis",
        "address": "1 Sand Dune Road, Oasis Town",
        "rooms": 30,
    },
    {
        "id": 5,
        "name": "Forest Retreat",
        "address": "55 Pine Cone Lane, Woodland",
        "rooms": 20,
    },
    {
        "id": 6,
        "name": "Urban Suites",
        "address": "200 Main Street, Big City",
        "rooms": 200,
    },
    {
        "id": 7,
        "name": "Lakeside Bungalows",
        "address": "10 Lake View, Waterton",
        "rooms": 15,
    },
    {
        "id": 8,
        "name": "Historic Grand Hotel",
        "address": "1 Old Town Square, Heritage City",
        "rooms": 80,
    },
    {
        "id": 9,
        "name": "Budget Towers",
        "address": "99 Cheap Street, Thriftyville",
        "rooms": 50,
    },
    {
        "id": 10,
        "name": "Luxury Towers",
        "address": "101 High Roller Ave, Richburg",
        "rooms": 300,
    },
]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    name: Optional[str] = Query(None, min_length=2, max_length=50),
    address: Optional[str] = Query(None, min_length=5, max_length=100),
):

    stop = pagination.page * pagination.per_page
    start = pagination.per_page * (pagination.page - 1)
    filtered_hotels = hotels

    if name:
        filtered_hotels = [
            h for h in filtered_hotels if name.lower() in h.get("name", "").lower()
        ]
    if address:
        filtered_hotels = [
            h
            for h in filtered_hotels
            if address.lower() in h.get("address", "").lower()
        ]
    return filtered_hotels[start:stop]


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
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.name,
            "address": hotel_data.address,
            "rooms": hotel_data.rooms,
        }
    )
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
