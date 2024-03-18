from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from cr_scraper.api.schema.model import Token
from cr_scraper.api.services.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    NotAuthenticatedError,
    authenticate_user,
    create_access_token,
)

templates = Jinja2Templates("cr_scraper/ui/templates")

router = APIRouter(tags=["sec"])


def get_token(form_data):
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except NotAuthenticatedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.username}, expires_delta=access_token_expires
    )

    return access_token


@router.post("/token")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    access_token = get_token(form_data)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/cookie")
async def login_ui(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    next: str | None = None,
    remember: Annotated[str, Form()] = "",
) -> RedirectResponse:
    access_token = get_token(form_data)
    cookie_attributes = f"token={access_token}; "
    cookie_attributes += "HttpOnly; SameSite=Lax; Secure; "
    if not remember:
        cookie_attributes += "Max-Age=30"
    return RedirectResponse(
        url=next or "/",
        headers={"Set-Cookie": cookie_attributes},
        status_code=HTTPStatus.SEE_OTHER,
    )


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, next: str | None = None):
    errors = {}
    return templates.TemplateResponse(
        name="login.html", context={"request": request, "next": next, "errors": errors}
    )
