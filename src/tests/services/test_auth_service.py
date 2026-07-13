import pytest
from src.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from src.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


@pytest.mark.asyncio
async def test_register_user_success(
    auth_service, user_create, mock_user_service, mock_password_service, user
):
    mock_user_service.get_user_by_email.return_value = None
    mock_password_service.hash_password.return_value = "hashed_password"
    mock_user_service.create_user.return_value = user

    result = await auth_service.register_user(user_create)

    assert result == user
    mock_user_service.get_user_by_email.assert_awaited_once_with(user_create.email)
    mock_password_service.hash_password.assert_called_once_with(user_create.password)
    mock_user_service.create_user.assert_awaited_once_with(
        name=user_create.name,
        email=user_create.email,
        password_hash="hashed_password",
    )


@pytest.mark.asyncio
async def test_register_user_already_exists(
    auth_service, user_create, mock_user_service, mock_password_service, user
):
    mock_user_service.get_user_by_email.return_value = user

    with pytest.raises(
        UserAlreadyExistsError, match="User with this email already exists"
    ):
        await auth_service.register_user(user_create)

    mock_user_service.get_user_by_email.assert_awaited_once_with(user_create.email)
    mock_password_service.hash_password.assert_not_called()
    mock_user_service.create_user.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_success(
    auth_service,
    mock_user_service,
    mock_password_service,
    mock_jwt_service,
    user_login,
    user,
):
    mock_user_service.get_user_by_email.return_value = user
    mock_password_service.verify_password.return_value = True
    mock_jwt_service.create_access_token.return_value = "access_token"
    mock_jwt_service.create_refresh_token.return_value = "refresh_token"

    result = await auth_service.authenticate_user(user_login)

    mock_user_service.get_user_by_email.assert_awaited_once_with(user_login.email)
    mock_password_service.verify_password.assert_called_once_with(
        user_login.password, user.password_hash
    )
    mock_jwt_service.create_access_token.assert_called_once_with(str(user.id))
    mock_jwt_service.create_refresh_token.assert_called_once_with(str(user.id))

    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(
    auth_service, mock_user_service, mock_password_service, mock_jwt_service, user_login
):
    mock_user_service.get_user_by_email.return_value = None

    with pytest.raises(InvalidCredentialsError, match="Invalid credentials"):
        await auth_service.authenticate_user(user_login)

    mock_user_service.get_user_by_email.assert_awaited_once_with(user_login.email)
    mock_password_service.verify_password.assert_not_called()
    mock_jwt_service.create_access_token.assert_not_called()
    mock_jwt_service.create_refresh_token.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(
    auth_service,
    mock_user_service,
    mock_password_service,
    mock_jwt_service,
    user_login,
    user,
):
    mock_user_service.get_user_by_email.return_value = user
    mock_password_service.verify_password.return_value = False

    with pytest.raises(InvalidCredentialsError, match="Invalid credentials"):
        await auth_service.authenticate_user(user_login)

    mock_user_service.get_user_by_email.assert_awaited_once_with(user_login.email)
    mock_password_service.verify_password.assert_called_once_with(
        user_login.password, user.password_hash
    )
    mock_jwt_service.create_access_token.assert_not_called()
    mock_jwt_service.create_refresh_token.assert_not_called()


@pytest.mark.asyncio
async def test_refresh_access_token_success(
    auth_service, mock_user_service, mock_jwt_service, user
):
    mock_jwt_service.decode_token.return_value = {"sub": str(user.id)}
    mock_user_service.get_user.return_value = user
    mock_jwt_service.create_access_token.return_value = "access_token"

    result = await auth_service.refresh_access_token("refresh_token")

    mock_jwt_service.decode_token.assert_called_once_with("refresh_token", "refresh")
    mock_user_service.get_user.assert_awaited_once_with(user.id)
    mock_jwt_service.create_access_token.assert_called_once_with(str(user.id))

    assert result.access_token == "access_token"
    assert result.refresh_token == "refresh_token"
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_refresh_access_token_invalid_token(
    auth_service, mock_user_service, mock_jwt_service
):
    mock_jwt_service.decode_token.side_effect = InvalidTokenError("Invalid token")

    with pytest.raises(InvalidTokenError, match="Invalid token"):
        await auth_service.refresh_access_token("invalid_token")

    mock_jwt_service.decode_token.assert_called_once_with("invalid_token", "refresh")
    mock_user_service.get_user.assert_not_called()
    mock_jwt_service.create_access_token.assert_not_called()


@pytest.mark.asyncio
async def test_refresh_access_token_expired_token(
    auth_service, mock_user_service, mock_jwt_service
):
    mock_jwt_service.decode_token.side_effect = ExpiredTokenError("Token expired")

    with pytest.raises(ExpiredTokenError, match="Token expired"):
        await auth_service.refresh_access_token("expired_token")

    mock_jwt_service.decode_token.assert_called_once_with("expired_token", "refresh")
    mock_user_service.get_user.assert_not_called()
    mock_jwt_service.create_access_token.assert_not_called()


@pytest.mark.asyncio
async def test_refresh_access_token_user_not_found(
    auth_service, mock_user_service, mock_jwt_service, user
):
    mock_jwt_service.decode_token.return_value = {"sub": str(user.id)}
    mock_user_service.get_user.side_effect = UserNotFoundError("User not found")

    with pytest.raises(UserNotFoundError, match="User not found"):
        await auth_service.refresh_access_token("refresh_token")

    mock_jwt_service.decode_token.assert_called_once_with("refresh_token", "refresh")
    mock_user_service.get_user.assert_awaited_once_with(user.id)
    mock_jwt_service.create_access_token.assert_not_called()
