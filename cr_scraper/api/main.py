from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from cr_scraper.api.router import api, security, ui
from cr_scraper.api.services.security import (
    DisabledUserError,
    NotAuthenticatedError,
    NotAuthorizedError,
)

app = FastAPI()
app.include_router(api.router)
app.include_router(ui.router)
app.include_router(security.router)
app.mount(
    "/static", StaticFiles(directory="cr_scraper/ui/templates/static"), name="static"
)


@app.exception_handler(NotAuthorizedError)
async def unauthorized_ui_user_handler(request: Request, ex: NotAuthorizedError):
    try:
        raise ex
    except NotAuthenticatedError:
        errors = "Wrong login or password"
    except DisabledUserError:
        errors = "User is disabled"
    except NotAuthorizedError:
        errors = "User does not have access to this resource"
    finally:
        return await security.login(
            request=request,
            next=request.url.path,
            errors=[errors],
        )
