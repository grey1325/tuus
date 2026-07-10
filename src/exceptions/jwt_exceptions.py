class JwtError(Exception):
    """Base class for JWT exceptions."""


class ExpiredTokenError(JwtError):
    """Raised when the token has expired."""


class InvalidTokenError(JwtError):
    """Raised when the token is invalid."""
