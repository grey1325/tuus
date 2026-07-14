import pytest

from src.exceptions.jwt_exceptions import InvalidTokenError
from src.dependencies import get_current_user
from src.exceptions.user_exceptions import UserNotFoundError


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
    with pytest.raises(UserNotFoundError, match=f"User {user.id} not found"):
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
    result = await service.create_user(
        name=user.name,
        email=user.email,
        password_hash=user.password_hash,
    )
    created_user = user_repo.create.call_args.args[0]
    assert result == user
    assert created_user.name == user.name
    assert created_user.email == user.email
    assert created_user.password_hash == user.password_hash


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


@pytest.mark.asyncio
async def test_get_current_user_success(mock_jwt_service, mock_user_service, user):
    mock_jwt_service.decode_token.return_value = {"sub": "1", "type": "access"}
    mock_user_service.get_user.return_value = user

    result = await get_current_user(
        token="token", jwt_service=mock_jwt_service, user_service=mock_user_service
    )

    mock_jwt_service.decode_token.assert_called_once_with("token", "access")
    mock_user_service.get_user.assert_awaited_once_with(1)

    assert result == user


@pytest.mark.asyncio
async def test_get_current_user_not_found(mock_jwt_service, mock_user_service):
    mock_jwt_service.decode_token.return_value = {"sub": "1", "type": "access"}
    mock_user_service.get_user.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError, match="User not found"):
        await get_current_user(
            token="token", jwt_service=mock_jwt_service, user_service=mock_user_service
        )

    mock_jwt_service.decode_token.assert_called_once_with("token", "access")
    mock_user_service.get_user.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_jwt_service, mock_user_service):
    mock_jwt_service.decode_token.side_effect = InvalidTokenError("Invalid token")

    with pytest.raises(InvalidTokenError, match="Invalid token"):
        await get_current_user(
            token="token", jwt_service=mock_jwt_service, user_service=mock_user_service
        )

    mock_jwt_service.decode_token.assert_called_once_with("token", "access")
    mock_user_service.get_user.assert_not_awaited()
