from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas import OrderStatus
from src.database.models import Order, OrderItem


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_id: int, total: float) -> Order:
        """Создание заказа."""
        order = Order(user_id=user_id, total=total)
        self.session.add(order)
        await self.session.flush()
        return order

    async def create_order_item(
        self, order_id: int, product_id: int, quantity: int
    ) -> OrderItem:
        """Создание товара в заказе."""
        order_item = OrderItem(
            order_id=order_id, product_id=product_id, quantity=quantity
        )
        self.session.add(order_item)
        await self.session.flush()
        return order_item

    async def get_by_id(self, order_id: int) -> Order | None:
        """Получение заказа по ID."""
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Order]:
        """Получение всех заказов."""
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.items).selectinload(OrderItem.product))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_status(self, order_id: int, status: OrderStatus) -> Order:
        """Обновление статуса заказа."""
        order = await self.get_by_id(order_id)
        assert order is not None
        order.status = status
        await self.session.flush()
        return order
