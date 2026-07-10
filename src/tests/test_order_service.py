from unittest.mock import call
import pytest
from src.api.schemas import OrderCreate, OrderItemCreate, OrderStatus


@pytest.mark.asyncio
async def test_empty_order(order_service_mock, user):
    service, _, _, _ = order_service_mock
    with pytest.raises(ValueError, match="Пустой заказ"):
        await service.create_order(OrderCreate(user_id=user.id, items=[]))


@pytest.mark.asyncio
async def test_user_not_found(order_service_mock, user, product):
    service, _, user_repo, _ = order_service_mock
    user_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match=f"Пользователь {user.id} не найден"):
        await service.create_order(
            OrderCreate(
                user_id=user.id,
                items=[OrderItemCreate(product_id=product.id, quantity=1)],
            )
        )


@pytest.mark.asyncio
async def test_product_not_found(order_service_mock, user, product):
    service, _, user_repo, product_repo = order_service_mock
    user_repo.get_by_id.return_value = user
    product_repo.get_by_ids.return_value = []
    with pytest.raises(ValueError, match=f"Товар {product.id} не найден"):
        await service.create_order(
            OrderCreate(
                user_id=user.id,
                items=[OrderItemCreate(product_id=product.id, quantity=1)],
            )
        )
    user_repo.get_by_id.assert_awaited_once_with(user.id)
    product_repo.get_by_ids.assert_awaited_once_with([product.id])


@pytest.mark.asyncio
async def test_create_order_success(order_service_mock, user, product, order):
    service, order_repo, user_repo, product_repo = order_service_mock
    user_repo.get_by_id.return_value = user
    product_repo.get_by_ids.return_value = [product]
    order_create = OrderCreate(
        user_id=1, items=[OrderItemCreate(product_id=product.id, quantity=1)]
    )
    order_repo.create_order.return_value = order
    result = await service.create_order(order_create)
    assert result == order
    expected_total = product.price * order_create.items[0].quantity
    user_repo.get_by_id.assert_awaited_once_with(user.id)
    product_repo.get_by_ids.assert_awaited_once_with([product.id])
    order_repo.create_order.assert_awaited_once_with(
        user_id=user.id, total=expected_total
    )
    order_repo.create_order_item.assert_awaited_once_with(
        order_id=order.id,
        product_id=product.id,
        quantity=order_create.items[0].quantity,
    )


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(order_service_mock, user, product):
    service, order_repo, user_repo, product_repo = order_service_mock
    user_repo.get_by_id.return_value = user
    product.stock = 1
    product_repo.get_by_ids.return_value = [product]
    order_create = OrderCreate(
        user_id=user.id, items=[OrderItemCreate(product_id=product.id, quantity=2)]
    )
    with pytest.raises(ValueError, match=f"Недостаточно товара {product.id} в наличии"):
        await service.create_order(order_create)
    user_repo.get_by_id.assert_awaited_once_with(user.id)
    product_repo.get_by_ids.assert_awaited_once_with([product.id])
    order_repo.create_order.assert_not_awaited()
    order_repo.create_order_item.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_order_multiple_products(
    order_service_mock, user, products, order
):
    service, order_repo, user_repo, product_repo = order_service_mock
    user_repo.get_by_id.return_value = user
    product_repo.get_by_ids.return_value = products
    order_create = OrderCreate(
        user_id=1,
        items=[
            OrderItemCreate(product_id=products[0].id, quantity=1),
            OrderItemCreate(product_id=products[1].id, quantity=2),
        ],
    )
    order_repo.create_order.return_value = order
    result = await service.create_order(order_create)
    assert result == order
    expected_total = (
        products[0].price * order_create.items[0].quantity
        + products[1].price * order_create.items[1].quantity
    )
    user_repo.get_by_id.assert_awaited_once_with(user.id)
    product_repo.get_by_ids.assert_awaited_once_with(
        [product.id for product in products]
    )
    order_repo.create_order.assert_awaited_once_with(
        user_id=user.id, total=expected_total
    )
    order_repo.create_order_item.assert_has_awaits(
        [
            call(
                order_id=order.id,
                product_id=products[0].id,
                quantity=order_create.items[0].quantity,
            ),
            call(
                order_id=order.id,
                product_id=products[1].id,
                quantity=order_create.items[1].quantity,
            ),
        ],
    )


@pytest.mark.asyncio
async def test_get_order_success(order_service_mock, order):
    service, order_repo, _, _ = order_service_mock
    order_repo.get_by_id.return_value = order
    result = await service.get_order(order.id)
    assert result == order
    order_repo.get_by_id.assert_awaited_once_with(order.id)


@pytest.mark.asyncio
async def test_get_order_not_found(order_service_mock, order):
    service, order_repo, _, _ = order_service_mock
    order_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match=f"Заказ {order.id} не найден"):
        await service.get_order(order.id)
    order_repo.get_by_id.assert_awaited_once_with(order.id)


@pytest.mark.asyncio
async def test_get_orders_success(order_service_mock, orders):
    service, order_repo, _, _ = order_service_mock
    order_repo.get_all.return_value = orders
    result = await service.get_orders()
    assert result == orders
    order_repo.get_all.assert_awaited_once_with(skip=0, limit=100)


@pytest.mark.asyncio
async def test_update_status_success(order_service_mock, order):
    service, order_repo, _, _ = order_service_mock
    new_status = OrderStatus.PAID
    order_repo.get_by_id.return_value = order
    order_repo.update_status.return_value = order
    result = await service.update_status(order.id, new_status)
    assert result == order
    order_repo.get_by_id.assert_awaited_once_with(order.id)
    order_repo.update_status.assert_awaited_once_with(order.id, new_status)


@pytest.mark.asyncio
async def test_update_status_not_found(order_service_mock, order):
    service, order_repo, _, _ = order_service_mock
    order_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match=f"Заказ {order.id} не найден"):
        await service.update_status(order.id, OrderStatus.PAID)
    order_repo.get_by_id.assert_awaited_once_with(order.id)
    order_repo.update_status.assert_not_awaited()
