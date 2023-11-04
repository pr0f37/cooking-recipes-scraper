"""
The following code maps business domain class objects to ORM table classes with
imperative mapper registry. Source:
https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#mapping-attrs-with-imperative-mapping
"""
from sqlalchemy.orm import registry

from cr_scraper.grocery_list.model import GroceryListElement
from cr_scraper.persistence.model import groceries

mapper_registry = registry()

mapper_registry.map_imperatively(GroceryListElement, groceries)
