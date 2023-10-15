import pytest

from cr_scraper.grocery_list.exceptions import NegativeQuantityError, TermMismatchError
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


def test_sum_up_different_objects():
    with pytest.raises(TermMismatchError):
        GroceryListElement("name1", 1, "kg") + 1


def test_add_groceries_of_the_same_kind():
    g = GroceryListElement("name1", 1, "kg")
    assert g + g == GroceryListElement("name1", 2, "kg")


def test_add_groceries_with_different_units():
    g1 = GroceryListElement("name1", 1, "kg")
    g2 = GroceryListElement("name1", 1, "g")
    assert g1 + g2 == [g1, g2]


def test_converting_units():
    g = GroceryListElement("name1", 1, "kg")
    assert g._can_convert("kg", "g") is True


def test_cannot_convert_units():
    g = GroceryListElement("name1", 1, "ml")
    assert g._can_convert("ml", "g") is False


def test_unit_init():
    _Unit = GroceryListElement.Unit
    assert _Unit("kg") is _Unit.KG
    assert _Unit("KG") is _Unit.KG
    assert _Unit("KG") == _Unit("kg")
    assert "test" != _Unit.KG
    with pytest.raises(ValueError):
        _Unit("test")
