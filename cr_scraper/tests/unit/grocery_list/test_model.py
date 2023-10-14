import pytest

from cr_scraper.grocery_list.exceptions import NegativeQuantityError
from cr_scraper.grocery_list.model import GroceryList, GroceryListElement


def test_create_empty_list():
    groceries = GroceryList()
    assert groceries.elements == dict()


def test_add_element():
    elem = GroceryListElement("name1", 1, "kg")
    groceries = GroceryList()
    groceries.add_element(elem)
    assert len(groceries.elements) == 1
    assert len(groceries.elements["name1"]) == 1


def test_add_multiple_elements():
    elem = GroceryListElement("name1", 1, "kg")
    groceries = GroceryList()
    groceries.add_element(elem)
    groceries.add_element(elem)
    assert len(groceries.elements) == 1
    assert len(groceries.elements["name1"]) == 2

    groceries.add_element(GroceryListElement("name2", 2, "ml"))
    assert len(groceries.elements) == 2
    assert len(groceries.elements["name1"]) == 2
    assert len(groceries.elements["name2"]) == 1


def test_create_negative_quantity_element():
    with pytest.raises(NegativeQuantityError):
        GroceryListElement("name1", -1, "kg")
