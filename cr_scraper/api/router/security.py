from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from cr_scraper.api.services.security import fake_hash_password, get_user

router = APIRouter(tags=["sec"])


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(form_data.username)
    if not user:
        raise HTTPException(400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}
