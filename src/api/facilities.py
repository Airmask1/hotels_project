import json
from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

# from src.setup import redis_manager
from src.utils.custom_cache import custom_cache

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@custom_cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.post("")
async def create_facilities(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(data=facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
