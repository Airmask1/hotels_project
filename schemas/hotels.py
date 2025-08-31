from pydantic import BaseModel, Field


class Hotel(BaseModel):
    name: str
    address: str
    rooms: int


class HotelPatch(BaseModel):
    name: str | None = Field(None)
    address: str | None = Field(None)
    rooms: int | None = Field(None)
