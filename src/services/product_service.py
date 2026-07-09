from src.api.schemas import ProductCreate, ProductUpdate
from src.database.repositories.product_repository import ProductRepository
from src.database.models import Product


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def get_product(self, product_id: int) -> Product:
        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")
        return product

    async def get_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        products = await self.product_repo.get_all(skip=skip, limit=limit)
        return products

    async def create_product(self, product: ProductCreate) -> Product:
        db_product = Product(
            name=product.name, price=product.price, stock=product.stock
        )
        return await self.product_repo.create(db_product)

    async def update_product(
        self, product_id: int, product_update: ProductUpdate
    ) -> Product:
        return await self.product_repo.update(product_id, product_update)

    async def search_products(
        self,
        name_query: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list[Product]:
        return await self.product_repo.search_products(name_query, min_price, max_price)

    async def delete_product(self, product_id: int) -> None:
        await self.product_repo.delete(product_id)
