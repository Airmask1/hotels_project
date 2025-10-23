from pydantic import BaseModel, ConfigDict, Field


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    model_config = ConfigDict(from_attributes=True)
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
