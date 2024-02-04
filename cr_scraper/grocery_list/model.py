from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Self
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

    def _convert(self, to_unit: Unit | str) -> float:
        return self.quantity / self._conversion_factor(to_unit)

    def add(self, other) -> Self:
        if not isinstance(other, GroceryListElement) or self.name != other.name:
            raise MismatchError
        self.quantity += other._convert(self.unit)
        return self

    def __add__(self, other) -> "GroceryListElement":
        if not isinstance(other, GroceryListElement) or self.name != other.name:
            raise MismatchError
        new = GroceryListElement(self.name, self.quantity, self.unit)
        new.quantity += other._convert(self.unit)
        return new

    def __eq__(self, other) -> bool:
        if not isinstance(other, GroceryListElement):
            raise MismatchError

        return all(
            getattr(self, elem) == getattr(other, elem)
            for elem in self.__dict__.keys() | other.__dict__.keys()
        )

    def _conversion_factor(self, unit: Unit | str):
        if self.unit == unit:
            return 1
        try:
            return UNIT_CONVERSION[Unit(unit)][self.unit]  # type: ignore
        except (KeyError, ValueError):
            raise CannotConvertError

    def convert_to(self, unit: Unit | str):
        self.quantity /= self._conversion_factor(unit)
        self.unit = unit
        return self


@dataclass
class GroceryList:
    id: UUID
    name: str | None = None
    groceries: list[GroceryListElement] = field(default_factory=list)

    def __init__(
        self,
        id: UUID | None = None,
        name: str | None = None,
        groceries: list[GroceryListElement] | None = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.groceries = groceries or []

    def add_element(self, new_element: GroceryListElement):
        if len(self.groceries) == 0:
            self.groceries.append(new_element)
        else:
            for idx, _ in enumerate(self.groceries):
                try:
                    self.groceries[idx].add(new_element)
                except (CannotConvertError, MismatchError):
                    continue
                return None
            self.groceries.append(new_element)
