from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, Tag


class RecipeComponents(ABC):
    @abstractmethod
    def __init__(self, parser: BeautifulSoup) -> None:
        self.parser = parser

    @abstractmethod
    def get_recipes_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_ingredients(self) -> list[tuple[str, float, str]]:
        raise NotImplementedError


class LidlComponents(RecipeComponents):
    def __init__(self, parser: BeautifulSoup) -> None:
        super().__init__(parser)

    def get_recipes_urls(self) -> list[str]:
        recipes = self.parser.find_all("a", class_="description")
        return [recipe["href"] for recipe in recipes]

    def get_title(self) -> str:
        return self._get_details().h1.text  # type: ignore

    def get_ingredients(self) -> list[tuple[str, float, str]]:
        ingredients = self._get_details().find(  # type: ignore
            "div", class_="skladniki"  # type: ignore
        )
        if isinstance(ingredients, Tag):
            return [
                self._parse_ingredient(li.text) for li in ingredients.find_all("li")
            ]  # type:ignore
        return []

    def _get_details(self):
        return self.parser.find("div", id="details")

    def _parse_ingredient(self, ingredient: str) -> tuple[str, float, str]:
        name, quantity_unit = ingredient.split("-")
        quantity, unit = quantity_unit.strip().split(" ")
        name = name.strip()
        quantity = float(quantity.strip().replace(",", "."))
        unit = unit.strip()
        return name, quantity, unit
