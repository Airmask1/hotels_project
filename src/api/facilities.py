from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from src.api.dependencies import DBDep, PaginationDep
from src.exceptions import MultipleObjectsFoundError, ObjectNotFoundError
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
    db: DBDep,
):

    return await db.facilities.get_all()


@router.post("")
async def create_facilities(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(data=facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
