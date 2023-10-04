from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import MissingSchema

from cr_scraper.scraper.exceptions import InvalidURLError
from cr_scraper.scraper.model import Recipe, RecipesSource
from cr_scraper.scraper.recipe_components import LidlComponents, RecipeComponents


def recipe_components_factory(url: str) -> RecipeComponents:
    source = RecipesSource.which_source(url)
    try:
        r = get(url)
    except MissingSchema:
        raise InvalidURLError(url)
    parser = BeautifulSoup(r.content, "html.parser")
    if source is RecipesSource.LIDL:
        return LidlComponents(parser)


def parse_recipe(url: str):
    recipe = recipe_components_factory(url)
    title = recipe.get_title()
    ingredients = recipe.get_ingredients()
    return Recipe(url=url, ingredients=ingredients, title=title)
