from http import HTTPStatus

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import MissingSchema

from cr_scraper.scraper.exceptions import (
    HTTPWebPageError,
    InvalidURLError,
    SourceNotRecognisedError,
)
from cr_scraper.scraper.model import Ingredient, Recipe, RecipesSource
from cr_scraper.scraper.recipe_components import LidlComponents, RecipeComponents


def recipe_components_factory(url: str) -> RecipeComponents:
    source = RecipesSource.which_source(url)
    try:
        r = get(url)
    except MissingSchema:
        raise InvalidURLError(url)
    if r.status_code != HTTPStatus.OK:
        raise HTTPWebPageError(url, r.status_code)
    parser = BeautifulSoup(r.content, "html.parser")
    if source is RecipesSource.LIDL:
        return LidlComponents(parser)
    raise SourceNotRecognisedError


def parse_recipe(url: str) -> Recipe:
    recipe = recipe_components_factory(url)
    title = recipe.get_title()
    ingredients = [
        Ingredient(name, quantity, unit)
        for name, quantity, unit in recipe.get_ingredients()
    ]
    return Recipe(url=url, ingredients=ingredients, title=title)
