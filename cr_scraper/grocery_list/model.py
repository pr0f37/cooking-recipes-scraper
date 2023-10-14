from collections import defaultdict
from dataclasses import dataclass

from cr_scraper.grocery_list.exceptions import NegativeQuantityError


@dataclass(init=False)
class GroceryListElement:
    name: str
    quantity: float
    unit: str

    def __init__(self, name: str, quantity: float, unit: str):
        if quantity < 0:
            raise NegativeQuantityError
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __add__(self, other):
        if not isinstance(other, GroceryListElement):
            raise KeyError
        if self.unit == other.unit:
            self.quantity += other.quantity


class GroceryList:
    def __init__(self):
        self.elements: dict[str, list[GroceryListElement]] = defaultdict(list)

    def add_element(self, element: GroceryListElement):
        self.elements[element.name].append(element)
