class UserAlreadyExistsError(Exception):
    """Raised when trying to register a user with an existing email."""


class UserNotFoundError(Exception):
    """Raised when a user is not found."""


class InvalidCredentialsError(Exception):
    """Raised when the provided credentials are invalid."""
