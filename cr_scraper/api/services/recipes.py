from uuid import UUID

from cr_scraper.grocery_list.model import GroceryList, GroceryListElement
from cr_scraper.persistence.repository import Repository, SQLRepository
from cr_scraper.scraper.model import Recipe
from cr_scraper.scraper.scraper import parse_recipe


def get_all_grocery_lists(repository: type[Repository] = SQLRepository):
    g_list = []
    with repository() as repo:
        g_list = repo.get(GroceryList)
    return g_list


def scrape_recipe(url: str) -> Recipe:
    recipe = parse_recipe(url)
    return recipe


def initialize_list(
    url: str, name: str, repository: type[Repository] = SQLRepository
) -> GroceryList:
    recipe = parse_recipe(url)
    groceries = GroceryList(name=name)
    add_recipe_to_list(groceries, recipe)
    id = groceries.id
    with repository() as repo:
        repo.add(groceries)
        repo.save()
    return get_list(id)


def update_list(
    url: str, id: UUID, repository: type[Repository] = SQLRepository
) -> GroceryList:
    recipe = parse_recipe(url)
    groceries = get_list(id)
    add_recipe_to_list(groceries, recipe)
    with repository() as repo:
        repo.add(groceries)
        repo.save()
    return get_list(id)


def get_list(id: UUID, repository: type[Repository] = SQLRepository) -> GroceryList:
    with repository() as repo:
        groceries = repo.get(GroceryList, id)
    return groceries


def add_recipe_to_list(groceries: GroceryList, recipe: Recipe) -> None:
    for ingredient in recipe.ingredients:
        groceries.add_element(
            GroceryListElement(ingredient.name, ingredient.quantity, ingredient.unit)
        )
