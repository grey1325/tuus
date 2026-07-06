from src.api.schemas import UserUpdate
from src.database.models import User
from src.database.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError(f"Пользователь {user_id} не найден")
        return user

    async def get_users(self, skip: int = 0, limit: int = 100):
        users = await self.user_repo.get_all(skip, limit)
        return users

    async def create_user(self, user):
        db_user = User(name=user.name, email=user.email)
        return await self.user_repo.create(db_user)

    async def update_user(self, user_id: int, user_update: UserUpdate):
        return await self.user_repo.update(user_id, user_update)

    async def delete_user(self, user_id: int):
        return await self.user_repo.delete(user_id)
