from fastapi import FastAPI
from pydantic import BaseModel

from cr_scraper.grocery_list.model import GroceryList
from cr_scraper.persistence.repository import SQLRepository
from cr_scraper.scraper.scraper import parse_recipe


class Url(BaseModel):
    url: str
    title: str = "my_list"


class GroceryListElementResponse(BaseModel):
    name: str
    quantity: float
    unit: str


class GroceryListResponse(BaseModel):
    name: str | None
    groceries: list[GroceryListElementResponse]


app = FastAPI()


@app.get("/", response_model=list[GroceryListResponse])
async def root():  # -> Any | list[Any] | None:
    g_list = []
    with SQLRepository() as repo:
        g_list = repo.get(GroceryList)
    return g_list


@app.post("/scrape")
async def scrape(url: Url):
    recipe = parse_recipe(url.url)
    grocery_list = GroceryList(name="my_list")
    for ingredient in recipe.ingredients:
        grocery_list.add_element(ingredient)
    with SQLRepository() as repo:
        repo.save(grocery_list)
        repo.commit()
