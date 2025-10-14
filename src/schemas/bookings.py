from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class BookingAdd(BaseModel):
    date_from: date
    date_to: date


class Booking(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    room_id: int
    user_id: int
    date_from: date
    price: int
    date_to: date


class BookingPatch(BaseModel):
    date_from: date | None = Field(None)
    date_to: date | None = Field(None)
