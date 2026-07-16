import json

from src.services.cache_service import CacheService
from src.api.schemas import ProductCreate, ProductResponse, ProductUpdate
from src.database.repositories.product_repository import ProductRepository
from src.database.models import Product


class ProductService:
    def __init__(self, product_repo: ProductRepository, cache_service: CacheService):
        self.product_repo = product_repo
        self.cache_service = cache_service

    async def get_product(self, product_id: int) -> ProductResponse:
        cache_key = f"product:{product_id}"

        cached = await self.cache_service.get(cache_key)
        if cached is not None:
            return ProductResponse.model_validate_json(cached)

        product = await self.product_repo.get_by_id(product_id)
        if product is None:
            raise ValueError(f"Товар {product_id} не найден")

        product_response = ProductResponse.model_validate(product)
        await self.cache_service.set(cache_key, product_response.model_dump_json())

        return product_response

    async def get_products(
        self, skip: int = 0, limit: int = 100
    ) -> list[ProductResponse]:
        cache_key = f"products:{skip}:{limit}"

        cached = await self.cache_service.get(cache_key)

        if cached is not None:
            products = json.loads(cached)
            return [ProductResponse.model_validate(product) for product in products]

        products = await self.product_repo.get_all(skip=skip, limit=limit)

        products_response = [
            ProductResponse.model_validate(product) for product in products
        ]

        await self.cache_service.set(
            cache_key,
            json.dumps([product.model_dump() for product in products_response]),
        )

        return products_response

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        db_product = Product(
            name=product.name, price=product.price, stock=product.stock
        )
        created_product = await self.product_repo.create(db_product)
        await self.cache_service.delete_pattern("products:*")
        return ProductResponse.model_validate(created_product)

    async def update_product(
        self, product_id: int, product_update: ProductUpdate
    ) -> ProductResponse:
        updated_product = await self.product_repo.update(product_id, product_update)
        await self.cache_service.delete(f"product:{product_id}")
        await self.cache_service.delete_pattern("products:*")
        return ProductResponse.model_validate(updated_product)

    async def search_products(
        self,
        name_query: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list[ProductResponse]:
        products = await self.product_repo.search_products(
            name_query, min_price, max_price
        )
        return [ProductResponse.model_validate(product) for product in products]

    async def delete_product(self, product_id: int) -> None:
        await self.product_repo.delete(product_id)
        await self.cache_service.delete(f"product:{product_id}")
        await self.cache_service.delete_pattern("products:*")
