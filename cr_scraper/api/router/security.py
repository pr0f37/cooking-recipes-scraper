from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from cr_scraper.api.schema.model import Token
from cr_scraper.api.services.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    can_create_user,
    create_access_token,
    create_user,
)

templates = Jinja2Templates("cr_scraper/ui/templates")

router = APIRouter(tags=["sec"])


def get_token(form_data: OAuth2PasswordRequestForm):
    user = authenticate_user(form_data.username, form_data.password)
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
    max_age = None
    if not remember:
        max_age = 360

    response = RedirectResponse(
        url=next or "/",
        status_code=HTTPStatus.SEE_OTHER,
    )
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=max_age,
    )
    return response


@router.post("/register")
async def register(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    next: str | None = None,
):
    username = form_data.username
    password = form_data.password
    errors = None
    success = None
    if can_create_user(username):
        _ = create_user(username, password)
        success = f"{username} user created!"
    else:
        errors = [f"{username} already exists, try a different username"]
    return await login(request, next, errors, success)


@router.get("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    next: str | None = None,
    errors: list | None = None,
    success: str | None = None,
):
    return templates.TemplateResponse(
        name="login.html",
        context={
            "request": request,
            "next": next,
            "errors": errors or [],
            "success": success,
        },
    )
