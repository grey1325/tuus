from src.database.models import Order
from src.database.repositories.product_repository import ProductRepository
from src.database.repositories.user_repository import UserRepository
from src.api.schemas import OrderCreate, OrderStatus
from src.database.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        user_repo: UserRepository,
        product_repo: ProductRepository,
    ):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.product_repo = product_repo

    async def create_order(self, order_data: OrderCreate):
        if not order_data.items:
            raise ValueError("Пустой заказ")
        user = await self.user_repo.get_by_id(order_data.user_id)
        if user is None:
            raise ValueError(f"Пользователь {order_data.user_id} не найден")
        product_ids = [item.product_id for item in order_data.items]
        products = await self.product_repo.get_by_ids(product_ids)
        print(products)
        products_map = {db_product.id: db_product for db_product in products}
        total = 0
        for item in order_data.items:
            product = products_map.get(item.product_id)
            if product is None:
                raise ValueError(f"Товар {item.product_id} не найден")
            if product.stock < item.quantity:
                raise ValueError(f"Недостаточно товара {item.product_id} в наличии")
            product.stock -= item.quantity
            total += product.price * item.quantity
        order = await self.order_repo.create_order(
            user_id=order_data.user_id, total=total
        )
        for item in order_data.items:
            await self.order_repo.create_order_item(
                order_id=order.id, product_id=item.product_id, quantity=item.quantity
            )
        return order

    async def get_order(self, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Заказ {order_id} не найден")
        return order

    async def get_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        orders = await self.order_repo.get_all(skip=skip, limit=limit)
        return orders

    async def update_status(self, order_id: int, status: OrderStatus) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if order is None:
            raise ValueError(f"Заказ {order_id} не найден")
        return await self.order_repo.update_status(order_id, status)
