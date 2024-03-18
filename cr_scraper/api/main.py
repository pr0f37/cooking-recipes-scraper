from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from cr_scraper.api.router import api, security, ui
from cr_scraper.api.schema.model import User
from cr_scraper.api.services.security import (
    UnauthorizedUIError,
    get_current_active_user,
    oauth2_scheme,
)

app = FastAPI()
app.include_router(api.router)
app.include_router(ui.router)
app.include_router(security.router)
app.mount(
    "/static", StaticFiles(directory="cr_scraper/ui/templates/static"), name="static"
)


@app.exception_handler(UnauthorizedUIError)
async def unauthorized_ui_user_handler(request: Request, ex: UnauthorizedUIError):
    return RedirectResponse(f"/login?next={request.url.path}")


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    try:
        return current_user
    except Exception:
        pass


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
