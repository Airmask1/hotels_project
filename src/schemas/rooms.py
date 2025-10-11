from pydantic import BaseModel, ConfigDict, Field


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class Room(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
