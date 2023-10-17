import pytest

from cr_scraper.grocery_list.exceptions import (
    CannotConvertError,
    MismatchError,
    NegativeQuantityError,
)
from cr_scraper.grocery_list.model import GroceryList, GroceryListElement, Unit


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
    assert len(groceries.elements["name1"]) == 1

    groceries.add_element(GroceryListElement("name2", 2, "ml"))
    assert len(groceries.elements) == 2
    assert len(groceries.elements["name1"]) == 1
    assert len(groceries.elements["name2"]) == 1


def test_add_multiple_elements_in_different_units():
    elem_kg = GroceryListElement("name1", 1, "kg")
    elem_g = elem_kg.convert_to(Unit.G)
    elem_l = GroceryListElement("name1", 1, "l")
    elem_hand = GroceryListElement("name1", 1, "handful")
    groceries = GroceryList()
    groceries.add_element(elem_kg)
    groceries.add_element(elem_l)
    groceries.add_element(elem_g)
    groceries.add_element(elem_hand)

    assert len(groceries.elements) == 1
    elem_name1 = groceries.elements["name1"]
    assert len(elem_name1) == 3
    assert [Unit.KG, Unit.L, "handful"] == [elem.unit for elem in elem_name1]
    assert [2, 1, 1] == [elem.quantity for elem in elem_name1]


def test_create_negative_quantity_element():
    with pytest.raises(NegativeQuantityError):
        GroceryListElement("name1", -1, "kg")


def test_sum_up_different_objects():
    with pytest.raises(MismatchError):
        GroceryListElement("name1", 1, "kg") + 1


def test_add_groceries_of_the_same_kind():
    g = GroceryListElement("name1", 1, "kg")
    assert g + g == GroceryListElement("name1", 2, "kg")


def test_add_groceries_with_different_units():
    g1 = GroceryListElement("name1", 1, "kg")
    g2 = GroceryListElement("name1", 1, "g")
    assert g1 + g2 == GroceryListElement("name1", 1.001, "kg")
    assert g2 + g1 == GroceryListElement("name1", 1001, "g")


def test_add_groceries_with_different_nonconvertible_units():
    g1 = GroceryListElement("name1", 1, "kg")
    g2 = GroceryListElement("name1", 1, "ml")
    with pytest.raises(CannotConvertError):
        g1 + g2
    with pytest.raises(CannotConvertError):
        g2 + g1


def test_converting_units():
    g = GroceryListElement("name1", 1, "kg")
    assert g._can_convert("g") is True


def test_cannot_convert_units():
    g = GroceryListElement("name1", 1, "ml")
    assert g._can_convert("g") is False


def test_convert_groceries():
    ml = GroceryListElement("name1", 1, "ml")
    assert ml.convert_to(Unit.L) == GroceryListElement("name1", 0.001, "l")
    li = GroceryListElement("name1", 1, "l")
    assert li.convert_to(Unit.ML) == GroceryListElement("name1", 1000, "ml")
    kg = GroceryListElement("name1", 1, "kg")
    assert kg.convert_to(Unit.G) == GroceryListElement("name1", 1000, "g")
    assert kg.convert_to(Unit.MG) == GroceryListElement("name1", 1000000, "mg")


def test_convert_groceries_error():
    ml = GroceryListElement("name1", 1, "ml")
    with pytest.raises(CannotConvertError):
        ml.convert_to(Unit.G)
    kg = GroceryListElement("name1", 1, "kg")
    with pytest.raises(CannotConvertError):
        kg.convert_to(Unit.L)


def test_unit_init():
    assert Unit("kg") is Unit.KG
    assert Unit("KG") is Unit.KG
    assert Unit("KG") is Unit("kg")
    assert "test" != Unit.KG
    with pytest.raises(ValueError):
        Unit("test")
