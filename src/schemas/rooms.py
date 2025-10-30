from pydantic import BaseModel, ConfigDict, Field


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None


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


class RoomPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = Field(None)
