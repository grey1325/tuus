import pytest


@pytest.mark.asyncio
async def test_user_success(user_service_mock, user):
    service, user_repo = user_service_mock
    user_repo.get_by_id.return_value = user
    result = await service.get_user(user.id)
    assert result == user
    user_repo.get_by_id.assert_awaited_once_with(user.id)


@pytest.mark.asyncio
async def test_get_user_not_found(user_service_mock, user):
    service, user_repo = user_service_mock
    user_repo.get_by_id.return_value = None
    with pytest.raises(ValueError, match=f"Пользователь {user.id} не найден"):
        await service.get_user(user.id)
    user_repo.get_by_id.assert_awaited_once_with(user.id)


@pytest.mark.asyncio
async def test_get_users_success(user_service_mock, users):
    service, user_repo = user_service_mock
    user_repo.get_all.return_value = users
    result = await service.get_users()
    assert result == users
    user_repo.get_all.assert_awaited_once_with(skip=0, limit=100)


@pytest.mark.asyncio
async def test_create_user_success(user_service_mock, user):
    service, user_repo = user_service_mock
    user_repo.create.return_value = user
    result = await service.create_user(user)
    created_user = user_repo.create.call_args.args[0]
    assert result == user
    assert created_user.name == user.name
    assert created_user.email == user.email


@pytest.mark.asyncio
async def test_update_user_success(user_service_mock, user, user_update):
    service, user_repo = user_service_mock
    user_repo.update.return_value = user_update
    result = await service.update_user(user.id, user_update)
    assert result == user_update
    user_repo.update.assert_awaited_once_with(user.id, user_update)


@pytest.mark.asyncio
async def test_delete_user_success(user_service_mock, user):
    service, user_repo = user_service_mock
    await service.delete_user(user.id)
    user_repo.delete.assert_awaited_once_with(user.id)
