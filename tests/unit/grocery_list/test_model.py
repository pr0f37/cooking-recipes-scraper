import pytest

from cr_scraper.grocery_list.exceptions import (
    CannotConvertError,
    MismatchError,
    NegativeQuantityError,
)
from cr_scraper.grocery_list.model import GroceryList, GroceryListElement, Unit


def test_create_empty_list():
    groceries = GroceryList()
    assert groceries.groceries == []


def test_add_element():
    elem = GroceryListElement("name1", 1, "kg")
    groceries = GroceryList()
    groceries.add_element(elem)
    assert len(groceries.groceries) == 1
    assert {grocery.name for grocery in groceries.groceries} == {"name1"}


def test_add_multiple_elements():
    elem = GroceryListElement("name1", 1, "kg")
    groceries = GroceryList()
    groceries.add_element(elem)
    groceries.add_element(elem)
    assert len(groceries.groceries) == 1

    groceries.add_element(GroceryListElement("name2", 2, "ml"))
    assert len(groceries.groceries) == 2
    assert {grocery.name for grocery in groceries.groceries} == {"name1", "name2"}


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

    gr_list = groceries.groceries
    assert len(gr_list) == 3
    assert {grocery.name for grocery in gr_list} == {"name1"}
    assert {Unit.KG, Unit.L, "handful"} == {elem.unit for elem in gr_list}
    assert [2, 1, 1] == [elem.quantity for elem in gr_list]


def test_create_negative_quantity_element():
    with pytest.raises(NegativeQuantityError):
        GroceryListElement("name1", -1, "kg")


def test_sum_up_different_objects():
    with pytest.raises(MismatchError):
        _ = GroceryListElement("name1", 1, "kg") + 1


def test_add_groceries_of_the_same_kind():
    g = GroceryListElement("name", 1, "kg")
    assert (g + g).name == "name"
    assert (g + g).quantity == 2
    assert (g + g).unit == Unit.KG
    assert (g + g).id != g.id


def test_add_groceries_with_different_units():
    g1 = GroceryListElement("name1", 1, "kg")
    g2 = GroceryListElement("name1", 1, "g")
    assert (g1 + g2).quantity == 1.001
    assert (g1 + g2).unit == Unit.KG
    assert (g2 + g1).quantity == 1001
    assert (g2 + g1).unit == Unit.G


def test_add_groceries_with_different_nonconvertible_units():
    g1 = GroceryListElement("name1", 1, "kg")
    g2 = GroceryListElement("name1", 1, "ml")
    with pytest.raises(CannotConvertError):
        _ = g1 + g2
    with pytest.raises(CannotConvertError):
        _ = g2 + g1


def test_converting_units():
    g = GroceryListElement("name1", 1, "kg")
    assert g._can_convert("g") is True


def test_cannot_convert_units():
    g = GroceryListElement("name1", 1, "ml")
    assert g._can_convert("g") is False


def test_convert_groceries():
    ml = GroceryListElement("name1", 1, "ml")
    assert ml.convert_to(Unit.L).unit == Unit.L
    assert ml.convert_to(Unit.L).quantity == 0.001
    li = GroceryListElement("name1", 1, "l")
    assert li.convert_to(Unit.ML).unit == Unit.ML
    assert li.convert_to(Unit.ML).quantity == 1000
    kg = GroceryListElement("name1", 1, "kg")
    assert kg.convert_to(Unit.G).unit == Unit.G
    assert kg.convert_to(Unit.G).quantity == 1000
    assert kg.convert_to(Unit.MG).unit == Unit.MG
    assert kg.convert_to(Unit.MG).quantity == 1000000


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
