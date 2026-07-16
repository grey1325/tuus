import json

import pytest

from src.api.schemas import ProductResponse


@pytest.mark.asyncio
async def test_get_product_from_cache(product_service_mock, product):
    service, product_repo, cache_service = product_service_mock
    expected = ProductResponse.model_validate(product)

    cache_service.get.return_value = expected.model_dump_json()
    result = await service.get_product(product.id)
    assert result == expected
    product_repo.get_by_id.assert_not_awaited()
    cache_service.get.assert_awaited_once_with(f"product:{product.id}")


@pytest.mark.asyncio
async def test_get_product_from_database(product_service_mock, product):
    service, product_repo, cache_service = product_service_mock
    expected = ProductResponse.model_validate(product)

    cache_service.get.return_value = None
    product_repo.get_by_id.return_value = product
    result = await service.get_product(product.id)
    cache_service.get.assert_awaited_once_with(f"product:{product.id}")
    product_repo.get_by_id.assert_awaited_once_with(product.id)
    cache_service.set.assert_awaited_once_with(
        f"product:{product.id}", expected.model_dump_json()
    )
    assert result == expected


@pytest.mark.asyncio
async def test_get_product_not_found(product_service_mock, product):
    service, product_repo, cache_service = product_service_mock
    cache_service.get.return_value = None
    product_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match=f"Товар {product.id} не найден"):
        await service.get_product(product.id)
    product_repo.get_by_id.assert_awaited_once_with(product.id)


@pytest.mark.asyncio
async def test_get_products_from_cache(product_service_mock, products):
    service, product_repo, cache_service = product_service_mock
    expected = [ProductResponse.model_validate(product) for product in products]
    cache_service.get.return_value = json.dumps(
        [product.model_dump() for product in expected]
    )

    result = await service.get_products()
    assert result == expected
    product_repo.get_all.assert_not_awaited()
    cache_service.get.assert_awaited_once_with("products:0:100")
    cache_service.set.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_products_from_database(product_service_mock, products):
    service, product_repo, cache_service = product_service_mock
    expected = [ProductResponse.model_validate(product) for product in products]
    cache_service.get.return_value = None

    product_repo.get_all.return_value = products
    result = await service.get_products()
    assert result == expected
    product_repo.get_all.assert_awaited_once_with(skip=0, limit=100)
    cache_service.get.assert_awaited_once_with("products:0:100")
    cache_service.set.assert_awaited_once_with(
        "products:0:100", json.dumps([product.model_dump() for product in expected])
    )


@pytest.mark.asyncio
async def test_create_product_success(product_service_mock, product):
    service, product_repo, cache_service = product_service_mock
    expected = ProductResponse.model_validate(product)
    product_repo.create.return_value = product

    result = await service.create_product(product)
    product_repo.create.assert_awaited_once()
    created_product = product_repo.create.call_args.args[0]

    assert created_product.name == product.name
    assert created_product.price == product.price
    assert created_product.stock == product.stock

    assert result == expected
    cache_service.delete_pattern.assert_awaited_once_with("products:*")


@pytest.mark.asyncio
async def test_update_product_success(product_service_mock, product, product_update):
    service, product_repo, cache_service = product_service_mock
    expected = ProductResponse.model_validate(product)
    product_repo.update.return_value = product

    result = await service.update_product(product.id, product_update)
    product_repo.update.assert_awaited_once_with(product.id, product_update)

    assert result == expected
    cache_service.delete.assert_awaited_once_with(f"product:{product.id}")
    cache_service.delete_pattern.assert_awaited_once_with("products:*")


@pytest.mark.asyncio
async def test_search_products_success(product_service_mock, products):
    service, product_repo, cache_service = product_service_mock
    expected = [ProductResponse.model_validate(product) for product in products]
    cache_service.get.return_value = None
    product_repo.search_products.return_value = products
    result = await service.search_products()
    assert result == expected
    product_repo.search_products.assert_awaited_once_with(None, None, None)


@pytest.mark.asyncio
async def test_delete_product_success(product_service_mock, product):
    service, product_repo, cache_service = product_service_mock
    await service.delete_product(product.id)
    product_repo.delete.assert_awaited_once_with(product.id)
    cache_service.delete.assert_awaited_once_with(f"product:{product.id}")
    cache_service.delete_pattern.assert_awaited_once_with("products:*")
