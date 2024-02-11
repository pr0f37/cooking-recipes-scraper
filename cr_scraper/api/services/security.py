from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from cr_scraper.api.schema.model import User, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password):
    return "fakehashed" + password


def get_user(username, db=fake_users_db):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def fake_decode_token(token):
    return get_user(token, fake_users_db)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="inactive user"
        )
    return current_user
