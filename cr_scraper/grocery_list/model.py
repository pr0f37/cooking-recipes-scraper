from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Self
from uuid import UUID, uuid4

from cr_scraper.grocery_list.exceptions import (
    CannotConvertError,
    MismatchError,
    NegativeQuantityError,
)


class Unit(StrEnum):
    KG = auto()
    G = auto()
    MG = auto()
    L = auto()
    ML = auto()

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


UNIT_CONVERSION = {
    Unit.KG: {Unit.G: 1000, Unit.MG: 1000000},
    Unit.G: {Unit.KG: 0.001, Unit.MG: 1000},
    Unit.MG: {Unit.KG: 0.000001, Unit.G: 0.001},
    Unit.L: {Unit.ML: 1000},
    Unit.ML: {Unit.L: 0.001},
}


@dataclass
class GroceryListElement:
    id: UUID
    name: str
    quantity: float
    unit: str

    def __init__(self, name: str, quantity: float, unit: str):
        self.id = uuid4()
        if quantity < 0:
            raise NegativeQuantityError
        self.name = name
        self.quantity = quantity
        try:
            self.unit = Unit(unit)
        except ValueError:
            self.unit = unit

    def __add__(self, other) -> Self:
        if not isinstance(other, GroceryListElement) or self.name != other.name:
            raise MismatchError
        converted = other.convert_to(self.unit)
        converted.quantity += self.quantity
        return converted

    def __eq__(self, other) -> bool:
        if not isinstance(other, GroceryListElement):
            raise MismatchError

        return all(
            getattr(self, elem) == getattr(other, elem)
            for elem in self.__dict__.keys() | other.__dict__.keys()
        )

    def _can_convert(self, unit: Unit | Any):
        return self.unit in UNIT_CONVERSION.get(unit, {}) or self.unit == unit

    def _conversion_factor(self, unit: Unit):
        if self.unit == unit:
            return 1
        return UNIT_CONVERSION[unit][self.unit]

    def convert_to(self, unit: Unit | Any):
        if self._can_convert(unit):
            quantity = self.quantity / self._conversion_factor(unit)
            return GroceryListElement(self.name, quantity, unit)
        else:
            raise CannotConvertError


class GroceryList:
    def __init__(self, name: str | None = None):
        self.id = uuid4()
        self.name: str | None = name
        self.groceries: list[GroceryListElement] = []

    def __repr__(self) -> str:
        return (
            f"GroceryList(id={self.id!r}, name={self.name!r}, "
            f"groceries={self.groceries!r}"
        )

    def add_element(self, new_element: GroceryListElement):
        if len(self.groceries) == 0:
            self.groceries.append(new_element)
        else:
            for idx, _ in enumerate(self.groceries):
                try:
                    self.groceries[idx] += new_element
                except (CannotConvertError, MismatchError):
                    continue
                return None
            self.groceries.append(new_element)
