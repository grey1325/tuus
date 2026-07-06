from sqlalchemy import select
from src.api.schemas import UserUpdate
from src.database.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по ID."""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """Получить всех пользователей."""
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, user: User) -> User:
        """Создать нового пользователя."""
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user_id: int, user_update: UserUpdate) -> User:
        """Обновить пользователя."""
        user = await self.get_by_id(user_id)
        if user is None:
            raise ValueError("Пользователь не найден")
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.session.flush()
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user is None:
            raise ValueError(f"Пользователь {user_id} не найден")
        await self.session.delete(user)
        await self.session.flush()
        print(f"User {user_id} deleted")
