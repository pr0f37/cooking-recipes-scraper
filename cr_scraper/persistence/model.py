from sqlalchemy import Column, Float, Integer, MetaData, String, Table
from sqlalchemy.orm import registry

from cr_scraper.grocery_list.model import GroceryListElement

metadata_obj = MetaData()
mapper_registry = registry()

groceries = Table(
    "groceries",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("quantity", Float, nullable=True),
    Column("unit", String, nullable=True),
)

mapper_registry.map_imperatively(GroceryListElement, groceries)
