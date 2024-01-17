from http import HTTPStatus
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from cr_scraper.api.schema.model import GroceryListResponse, Url, UrlAndTitle
from cr_scraper.api.services.recipes import (
    delete_list,
    get_all_grocery_lists,
    get_list,
    initialize_list,
    scrape_recipe,
    search_for_grocery_list,
    update_list,
    update_list_add_recipe,
)
from cr_scraper.grocery_list.model import GroceryList
from cr_scraper.persistence.repository import NotExistInRepositoryError
from cr_scraper.scraper.model import Recipe

templates = Jinja2Templates("cr_scraper/ui/templates")
app = FastAPI()


@app.get("/")
async def index():
    return RedirectResponse("/grocery_lists/html")


@app.post("/recipes/scrape")
async def scrape(url: Url) -> Recipe:
    return scrape_recipe(str(url.url))


@app.get("/grocery_lists", response_model=list[GroceryListResponse])
async def display_all_grocery_lists():  # -> Any | list[Any] | None:
    return get_all_grocery_lists()


@app.get("/grocery_lists/html", response_class=HTMLResponse)
async def show_grocery_lists(request: Request, q: str | None = None):
    if q:
        grocery_lists = search_for_grocery_list(list_name=q)
    else:
        grocery_lists = get_all_grocery_lists()
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "grocery_lists": grocery_lists, "q": q},
    )


@app.post("/grocery_lists/html", response_class=HTMLResponse)
async def show_grocery_lists_partial(request: Request):
    async with request.form() as form:
        q = form["q"]
    if q:
        grocery_lists = search_for_grocery_list(list_name=q)
        return templates.TemplateResponse(
            name="grocery_list/partial_search_results.html",
            context={"request": request, "grocery_lists": grocery_lists},
        )


@app.post(
    "/grocery_lists",
    status_code=HTTPStatus.CREATED,
    response_model=GroceryListResponse,
)
async def new_list(url: UrlAndTitle):
    return initialize_list(str(url.url), url.title)


@app.get(
    "/grocery_lists/{id}",
    status_code=HTTPStatus.OK,
    response_model=GroceryListResponse,
)
async def get_grocery_list(id: UUID):
    try:
        return get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")


@app.get(
    "/grocery_lists/{id}/html",
    status_code=HTTPStatus.OK,
)
async def get_grocery_list_html(request: Request, id: UUID):
    try:
        grocery_list = get_list(id)
        return templates.TemplateResponse(
            name="grocery_list/show.html",
            context={"request": request, "grocery_list": grocery_list},
        )
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")


@app.get("/grocery_lists/{id}/add_recipe/html")
async def add_recipe_to_list_view(request: Request, id: UUID):
    try:
        grocery_list = get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")
    return templates.TemplateResponse(
        name="grocery_list/add_recipe.html",
        context={"request": request, "grocery_list": grocery_list},
    )


@app.post(
    "/grocery_lists/{id}/add_recipe",
    status_code=HTTPStatus.CREATED,
    response_model=GroceryListResponse,
)
async def add_recipe_to_groceries_list(url: Url, id: UUID):
    try:
        return update_list_add_recipe(str(url.url), id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")


@app.post(
    "/grocery_lists/{id}/add_recipe/html",
    status_code=HTTPStatus.CREATED,
    response_model=GroceryListResponse,
)
async def add_recipe_to_groceries_list_html(request: Request, id: UUID):
    async with request.form() as form:
        url = Url(url=form["url"])
    try:
        _ = update_list_add_recipe(str(url.url), id)
        return RedirectResponse("/grocery_lists/html", status_code=303)
    except NotExistInRepositoryError:
        return templates.TemplateResponse(
            name="grocery_list/add_recipe.html",
            context={
                "request": request,
                "grocery_list": GroceryList(id=id, name="Not exist", groceries=[]),
                "errors": f"List with id={id} does not exist",
            },
        )


@app.get("/grocery_lists/{id}/edit/html")
async def edit_grocery_list_html(request: Request, id: UUID):
    try:
        grocery_list = get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")

    return templates.TemplateResponse(
        name="grocery_list/edit.html",
        context={"request": request, "grocery_list": grocery_list},
    )


@app.post("/grocery_lists/{id}/edit/html")
async def edit_grocery_list_html_post(request: Request, id: UUID):
    try:
        async with request.form() as form:
            name = str(form["list_name"])
        _ = update_list(id=id, name=name, groceries=[])
    except NotExistInRepositoryError:
        return templates.TemplateResponse(
            name="grocery_list/edit.html",
            context={
                "request": request,
                "grocery_list": GroceryList(id=id, name="Not exist", groceries=[]),
                "errors": f"Grocery list {id} not exists",
            },
        )

    return RedirectResponse(f"/grocery_lists/{id}/html", status_code=303)


@app.post("/grocery_lists/{id}/delete/html", status_code=HTTPStatus.NO_CONTENT)
async def delete_grocery_list_html(request: Request, id: UUID):
    delete_list(id)
    return RedirectResponse("/grocery_lists/html", status_code=HTTPStatus.SEE_OTHER)
