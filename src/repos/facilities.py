from datetime import date

from sqlalchemy import func, insert, select

from src.models.facilities import FacilitiesOrm
from src.repos.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
