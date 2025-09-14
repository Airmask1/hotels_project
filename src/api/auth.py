from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from src.database import async_session_maker
from src.exceptions import UserAlreadyExists
from src.repos.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {"status": "OK"}
        except UserAlreadyExists:
            raise HTTPException(status_code=500, detail="User already exists")
