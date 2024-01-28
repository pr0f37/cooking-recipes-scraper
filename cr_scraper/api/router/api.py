from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from cr_scraper.api.schema.model import GroceryListResponse, Url, UrlAndTitle
from cr_scraper.api.services.recipes import (
    get_all_grocery_lists,
    get_list,
    initialize_list,
    scrape_recipe,
    update_list_add_recipe,
)
from cr_scraper.persistence.repository import NotExistInRepositoryError
from cr_scraper.scraper.model import Recipe

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/recipes/scrape")
async def scrape(url: Url) -> Recipe:
    return scrape_recipe(str(url.url))


@router.get("/grocery_lists", response_model=list[GroceryListResponse])
async def display_all_grocery_lists():  # -> Any | list[Any] | None:
    return get_all_grocery_lists()


@router.post(
    "/grocery_lists",
    status_code=HTTPStatus.CREATED,
    response_model=GroceryListResponse,
)
async def new_list(url: UrlAndTitle):
    return initialize_list(str(url.url), url.title)


@router.get(
    "/grocery_lists/{id}",
    status_code=HTTPStatus.OK,
    response_model=GroceryListResponse,
)
async def get_grocery_list(id: UUID):
    try:
        return get_list(id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")


@router.post(
    "/grocery_lists/{id}/add_recipe",
    status_code=HTTPStatus.CREATED,
    response_model=GroceryListResponse,
)
async def add_recipe_to_groceries_list(url: Url, id: UUID):
    try:
        return update_list_add_recipe(str(url.url), id)
    except NotExistInRepositoryError:
        raise HTTPException(HTTPStatus.NOT_FOUND, f"Grocery list {id} not exists")
