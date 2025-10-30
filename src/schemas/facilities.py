from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FacilityPatch(BaseModel):
    title: str | None = Field(None)


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
