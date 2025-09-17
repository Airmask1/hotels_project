from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    data = AuthService().decode_token(encoded_token=token)
    user_id = data.get("user_id")
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
