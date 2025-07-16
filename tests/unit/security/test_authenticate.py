from cr_scraper.api.services.security import (
    verify_password,
    get_password_hash,
    get_user,
    create_user,
    authenticate_user,
)


def test_verify_password():
    pwd = "password"
    pwd_hash = get_password_hash(pwd)
    assert isinstance(pwd_hash, str)
    assert verify_password(pwd, pwd_hash) is True


def test_verify_password_wrong():
    pwd = "password"
    pwd_hash = get_password_hash(pwd)
    assert isinstance(pwd_hash, str)
    assert verify_password("wrong_password", pwd_hash) is False


def test_get_password_hash():
    pwd = "password"
    pwd_hash = get_password_hash(pwd)
    assert isinstance(pwd_hash, str)
    assert len(pwd_hash) > 0


def test_get_user():
    user = get_user("johndoe")
    assert user.username == "johndoe"


def test_create_new_user():
    user = create_user("test", "password")
    assert authenticate_user("test", "password") == user
