from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from cr_scraper.api.router import api, ui

app = FastAPI()
app.include_router(api.router)
app.include_router(ui.router)
app.mount(
    "/static", StaticFiles(directory="cr_scraper/ui/templates/static"), name="static"
)
