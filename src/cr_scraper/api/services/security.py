from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from cr_scraper.api.schema.model import TokenData, User, UserInDB

SECRET_KEY = "6c0f94d9009420305a45debe7f770d3411b1dac2bf1bd095dd7ada9221d6c915"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_cookie = OAuth2PasswordBearer(tokenUrl="cookie")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$Mx0RlslMiAOrgoydW/bSoeEjBuUpmntTHRWU8P2dbcH5ubwSGSgXq",
        "disabled": False,
    }
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(username: str, password: str, db=fake_users_db) -> UserInDB:
    hashed_password = get_password_hash(password)
    db[username] = {
        "username": username,
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return UserInDB(**db[username])


def can_create_user(username: str, db=fake_users_db) -> bool:
    try:
        _ = get_user(username, db)
    except KeyError:
        return True
    return False


def authenticate_user(username: str, password: str, db=fake_users_db) -> UserInDB:
    try:
        user = get_user(username, db)
    except KeyError:
        raise NotAuthenticatedError
    if not verify_password(password, user.hashed_password):
        raise NotAuthenticatedError
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(username, db=fake_users_db):
    user_dict = db[username]
    return UserInDB(**user_dict)


def _get_current_user(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str | None = payload.get("sub")
    token_data = TokenData(username=username)
    user = get_user(token_data.username)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = NotAuthenticatedError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = _get_current_user(token)
    except (KeyError, JWTError):
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive user"
        )
    return current_user


async def get_current_active_user_auth_cookie(
    token: Annotated[str | None, Cookie()] = None,
):
    if not token:
        raise NotAuthenticatedError
    try:
        current_user = _get_current_user(token)
    except (KeyError, JWTError):
        raise NotAuthenticatedError
    if current_user.disabled:
        raise DisabledUserError
    return current_user


class NotAuthorizedError(HTTPException):
    def __init__(
        self, status_code: int = 401, detail=None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status_code, detail, headers)


class NotAuthenticatedError(NotAuthorizedError):
    pass


class DisabledUserError(NotAuthorizedError):
    pass
