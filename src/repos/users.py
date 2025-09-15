from sqlalchemy import insert, select

from src.exceptions import UserAlreadyExists
from src.models.users import UsersOrm
from src.repos.base import BaseRepository
from src.schemas.users import User, UserAdd, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add(self, data: UserAdd):
        existing_user = await self.get_one_or_none(email=data.email)
        if existing_user:
            raise UserAlreadyExists("User with this email already exists")
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        await self.session.scalars(add_stmt)

    async def get_user_with_hashed_password(self, email: str):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model:
            return UserWithHashedPassword.model_validate(model, from_attributes=True)
        return None
