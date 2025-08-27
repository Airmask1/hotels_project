from fastapi import Body, FastAPI, HTTPException

app = FastAPI()


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
]


@app.put("/hotels/{hotel_id}")
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


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    name: str | None = Body(default=None),
    address: str | None = Body(default=None),
    rooms: int | None = Body(default=None),
):
    global hotels
    for h in hotels:
        if h.get("id") == hotel_id:
            if name:
                h["name"] = name
            if address:
                h["address"] = address
            if rooms:
                h["rooms"] = rooms
            return h

    raise HTTPException(status_code=404, detail="Hotel not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
