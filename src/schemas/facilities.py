from pydantic import BaseModel, ConfigDict, Field


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FacilityPatch(BaseModel):
    title: str | None = Field(None)
