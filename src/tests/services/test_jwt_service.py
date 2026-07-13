import pytest

from src.services.jwt_service import JwtService
from src.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError


def test_create_access_token_success(jwt_service):
    subject = "test"

    token = jwt_service.create_access_token(subject)
    payload = jwt_service.decode_token(token, "access")

    assert isinstance(token, str)
    assert payload["sub"] == subject
    assert payload["type"] == "access"
    assert isinstance(payload["exp"], int)
    assert isinstance(payload["iat"], int)


def test_create_refresh_token_success(jwt_service):
    subject = "test"

    token = jwt_service.create_refresh_token(subject)
    payload = jwt_service.decode_token(token, "refresh")

    assert isinstance(token, str)
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"
    assert isinstance(payload["exp"], int)
    assert isinstance(payload["iat"], int)


def test_decode_expired_access_token():
    jwt_service = JwtService(access_token_expire_minutes=-1)

    token = jwt_service.create_access_token("test")

    with pytest.raises(ExpiredTokenError):
        jwt_service.decode_token(token, "access")


def test_decode_invalid_token(jwt_service):
    with pytest.raises(InvalidTokenError):
        jwt_service.decode_token("not-a-jwt", "access")


def test_decode_unexpected_token_type(jwt_service):

    token = jwt_service.create_access_token("test")

    with pytest.raises(InvalidTokenError):
        jwt_service.decode_token(token, "invalid_token")


def test_decode_refresh_token_as_access_token(jwt_service):

    token = jwt_service.create_refresh_token("test")

    with pytest.raises(InvalidTokenError):
        jwt_service.decode_token(token, "access")


def test_decode_access_token_as_refresh_token(jwt_service):

    token = jwt_service.create_access_token("test")

    with pytest.raises(InvalidTokenError):
        jwt_service.decode_token(token, "refresh")
