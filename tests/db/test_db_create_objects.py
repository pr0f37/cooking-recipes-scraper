from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from cr_scraper.grocery_list.model import GroceryList, GroceryListElement, Unit
from cr_scraper.persistence.model import metadata_obj
from cr_scraper.persistence.repository import SQLRepository
import pytest


@pytest.mark.database
def test_create_tables():
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@0.0.0.0:5432/cr-scraper", echo=True
    )
    metadata_obj.create_all(engine, checkfirst=True)

    grocery = GroceryListElement(name="test_name", quantity=1.02, unit=Unit.KG)
    grocery_list = GroceryList(name="test list")
    grocery_list.add_element(grocery)
    grocery_list.add_element(grocery)
    with Session(engine) as session:
        session.add(grocery_list)
        session.commit()


@pytest.mark.database
def test_get_data():
    with SQLRepository() as repo:
        all_grocery_lists = repo.get_all(GroceryList)
        groceries = repo.get_all(GroceryListElement)

    for g_list in all_grocery_lists:
        assert isinstance(g_list, GroceryList)

    for g in groceries:
        assert isinstance(g, GroceryListElement)
