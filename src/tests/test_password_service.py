def test_hash_password_returns_string(password_service):
    hashed_password = password_service.hash_password("password")
    assert isinstance(hashed_password, str)


def test_hash_password_returns_hashed_value(password_service):
    hashed_password = password_service.hash_password("password")
    assert hashed_password != "password"


def test_verify_password_returns_true_for_valid_password(password_service):
    hashed_password = password_service.hash_password("password")
    assert password_service.verify_password("password", hashed_password)


def test_verify_password_returns_false_for_invalid_password(password_service):
    hashed_password = password_service.hash_password("password")
    assert not password_service.verify_password("wrong_password", hashed_password)


def test_same_password_generates_different_hashes(password_service):
    hashed_password1 = password_service.hash_password("password")
    hashed_password2 = password_service.hash_password("password")
    assert hashed_password1 != hashed_password2
