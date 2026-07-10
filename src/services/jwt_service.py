from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from src.exceptions.jwt_exceptions import ExpiredTokenError, InvalidTokenError
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)


class JwtService:
    def __init__(
        self,
        secret_key: str | None = None,
        algorithm: str = JWT_ALGORITHM,
        access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> None:
        if secret_key is None:
            secret_key = SECRET_KEY
        self._secret_key: str = secret_key
        self._algorithm = algorithm
        self._access_token_expire_minutes = access_token_expire_minutes
        self._refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(self, subject: str) -> str:
        lifetime = timedelta(minutes=self._access_token_expire_minutes)
        return self._create_token(subject, "access", lifetime)

    def create_refresh_token(self, subject: str) -> str:
        lifetime = timedelta(days=self._refresh_token_expire_days)
        return self._create_token(subject, "refresh", lifetime)

    def _create_token(self, subject: str, token_type: str, lifetime: timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "type": token_type,
            "exp": now + lifetime,
            "iat": now,
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str, expected_type: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            if payload.get("type") != expected_type:
                raise InvalidTokenError("Unexpected token type")
            return payload
        except jwt.ExpiredSignatureError as exc:
            raise ExpiredTokenError("Token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise InvalidTokenError("Unexpected token type") from exc
