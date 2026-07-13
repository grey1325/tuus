from src.exceptions.user_exceptions import UserNotFoundError
from src.api.schemas import UserUpdate
from src.database.models import User
from src.database.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User {user_id} not found")
        return user

    async def get_users(self, skip: int = 0, limit: int = 100):
        users = await self.user_repo.get_all(skip=skip, limit=limit)
        return users

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repo.get_by_email(email)

    async def create_user(self, name: str, email: str, password_hash: str) -> User:
        db_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
        )
        return await self.user_repo.create(db_user)

    async def update_user(self, user_id: int, user_update: UserUpdate):
        return await self.user_repo.update(user_id, user_update)

    async def delete_user(self, user_id: int):
        return await self.user_repo.delete(user_id)
