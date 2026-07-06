from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ProductUpdate
from src.database.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        """Получить товар по ID."""
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, product_ids: list[int]) -> list[Product]:
        """Получить товары по ID."""
        result = await self.session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        return list(result.scalars().all())

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        """Получить список товаров с пагинацией."""
        result = await self.session.execute(select(Product).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, product: Product) -> Product:
        """Создать новый товар."""
        self.session.add(product)
        await self.session.flush()
        return product

    async def update(self, product_id: int, product_update: ProductUpdate) -> Product:
        """Обновить товар."""
        product = await self.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        await self.session.flush()
        return product

    async def update_stock(
        self,
        product_id: int,
        quantity_delta: int,
    ) -> None:
        """Обновить остаток товара."""
        product = await self.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")
        product.stock += quantity_delta

    async def search_products(
        self,
        name_query: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list[Product]:
        """Поиск товаров по названию."""
        query = select(Product)
        if name_query is not None:
            query = query.where(Product.name.contains(name_query))
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)

        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def delete(self, product_id: int) -> None:
        product = await self.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")

        await self.session.delete(product)
        await self.session.flush()
        print(f"Product {product_id} deleted")
