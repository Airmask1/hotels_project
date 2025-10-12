from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserAlreadyExists
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user or not AuthService().verify_password(
        plain_password=data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect user or password")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}
    except UserAlreadyExists:
        raise HTTPException(status_code=500, detail="User already exists")


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "logged out"}
