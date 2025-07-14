from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from cr_scraper.api.schema.model import Url, UrlAndTitle
from cr_scraper.api.services.recipes import (
    delete_list,
    get_all_grocery_lists,
    get_list,
    initialize_list,
    search_for_grocery_list,
    update_list,
    update_list_add_recipe,
)
from cr_scraper.api.services.security import get_current_active_user_auth_cookie
from cr_scraper.archiver import Archiver
from cr_scraper.grocery_list.model import GroceryList
from cr_scraper.persistence.repository import NotExistInRepositoryError

templates = Jinja2Templates("src/cr_scraper/ui/templates")
router = APIRouter(
    tags=["ui"], dependencies=[Depends(get_current_active_user_auth_cookie)]
)


@router.get("/")
async def index():
    return RedirectResponse("/grocery_lists")


@router.post("/recipes/scrape")
async def url_validate(url: Annotated[str, Form()] = ""):
    try:
        _ = Url(url=url)  # type: ignore
        return Response(content="URL OK!")
    except ValidationError as ex:
        return Response(content=", ".join([er["msg"] for er in ex.errors()]))


@router.get("/grocery_lists", response_class=HTMLResponse)
async def show_grocery_lists(
    request: Request,
    hx_trigger: Annotated[str | None, Header()] = None,
    q: str | None = None,
    page: int = 1,
):
    errors = {}
    if q:
        grocery_lists = search_for_grocery_list(list_name=q)
        if hx_trigger == "search":
            return templates.TemplateResponse(
                name="grocery_list/rows.html",
                context={"request": request, "grocery_lists": grocery_lists},
            )
    else:
        grocery_lists = get_all_grocery_lists(page=page - 1)
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "grocery_lists": grocery_lists,
            "errors": errors,
            "page": page,
            "archiver": Archiver.get(),
        },
    )


@router.get("/grocery_lists/count")
async def count_all_grocery_lists(request: Request):
    count = len(get_all_grocery_lists())
    return Response(content=f"({count} lists total)")


@router.post(
    "/grocery_lists/new",
    status_code=HTTPStatus.CREATED,
)
async def new_list_html(
    url: Annotated[str, Form()] = "",
    name: Annotated[str, Form()] = "",
):
    uat = UrlAndTitle(url=url, title=name)  # type: ignore

    initialize_list(str(uat.url), uat.title)
    return RedirectResponse("/grocery_lists", status_code=HTTPStatus.SEE_OTHER)


@router.get("/grocery_lists/archive", response_class=HTMLResponse)
async def archive_status(request: Request):
    archiver = Archiver.get()
    return templates.TemplateResponse(
        name="grocery_list/archive_ui.html",
        context={"request": request, "archiver": archiver},
    )


@router.get("/grocery_lists/archive/file")
async def archive_content():
    manager = Archiver.get()
    return FileResponse(
        manager.archive_file(),
        media_type="application/octet-stream",
        filename="archive.json",
    )


@router.get(
    "/grocery_lists/{id}", status_code=HTTPStatus.OK, response_class=HTMLResponse
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


@router.get("/grocery_lists/{id}/add_recipe", response_class=HTMLResponse)
async def add_recipe_to_list_view(request: Request, id: UUID):
    try:
        grocery_list = get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")
    return templates.TemplateResponse(
        name="grocery_list/add_recipe.html",
        context={"request": request, "grocery_list": grocery_list},
    )


@router.post(
    "/grocery_lists/{id}/add_recipe",
    status_code=HTTPStatus.CREATED,
    response_class=HTMLResponse,
)
async def add_recipe_to_groceries_list_html(
    request: Request, id: UUID, url: Annotated[str, Form()] = ""
):
    parsed_url = Url(url=url)  # type: ignore
    try:
        _ = update_list_add_recipe(str(parsed_url.url), id)
        return RedirectResponse(f"/grocery_lists/{id}", status_code=303)
    except NotExistInRepositoryError:
        return templates.TemplateResponse(
            name="grocery_list/add_recipe",
            context={
                "request": request,
                "grocery_list": GroceryList(id=id, name="Not exist"),
                "errors": f"List with id={id} does not exist",
            },
        )


@router.get("/grocery_lists/{id}/edit", response_class=HTMLResponse)
async def edit_grocery_list_html(request: Request, id: UUID):
    try:
        grocery_list = get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")

    return templates.TemplateResponse(
        name="grocery_list/edit.html",
        context={"request": request, "grocery_list": grocery_list},
    )


@router.post(
    "/grocery_lists/{id}/edit",
    response_class=HTMLResponse,
)
async def edit_grocery_list_html_post(
    request: Request, id: UUID, list_name: Annotated[str, Form()]
):
    try:
        _ = update_list(id=id, name=list_name, groceries=[])
    except NotExistInRepositoryError:
        return templates.TemplateResponse(
            name="grocery_list/edit.html",
            context={
                "request": request,
                "grocery_list": GroceryList(id=id, name="Not exist"),
                "errors": f"Grocery list {id} not exists",
            },
        )

    return RedirectResponse(f"/grocery_lists/{id}", status_code=303)


@router.delete(
    "/grocery_lists/archive",
    response_class=HTMLResponse,
)
async def clear_archive(request: Request):
    archiver = Archiver.get()
    archiver.reset()
    return templates.TemplateResponse(
        name="grocery_list/archive_ui.html",
        context={"request": request, "archiver": archiver},
    )


@router.delete("/grocery_lists/{id}")
async def delete_grocery_list_html(
    id: UUID, hx_trigger: Annotated[str | None, Header()] = None
):
    delete_list(id)
    if hx_trigger == "delete-btn":
        return RedirectResponse("/grocery_lists", status_code=HTTPStatus.SEE_OTHER)
    return Response(content="")


@router.delete("/grocery_lists")
async def delete_all_grocery_lists_html(
    selected_list_ids: Annotated[list[UUID], Form()],
):
    for id in selected_list_ids:
        delete_list(id)
    return RedirectResponse("/grocery_lists", status_code=HTTPStatus.SEE_OTHER)


@router.post("/grocery_lists/archive", response_class=HTMLResponse)
async def start_archive(request: Request):
    archiver = Archiver.get()
    archiver.run()
    return templates.TemplateResponse(
        name="grocery_list/archive_ui.html",
        context={"request": request, "archiver": archiver},
    )
