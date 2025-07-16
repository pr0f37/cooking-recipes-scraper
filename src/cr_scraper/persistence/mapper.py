"""
The following code maps business domain class objects to ORM table classes with
imperative mapper registry. Source:
https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#mapping-attrs-with-imperative-mapping
"""

from sqlalchemy.orm import registry, relationship

from cr_scraper.grocery_list.model import GroceryList, GroceryListElement
from cr_scraper.persistence.model import groceries, grocery_lists

mapper_registry = registry()

mapper_registry.map_imperatively(
    GroceryList,
    grocery_lists,
    properties={
        "groceries": relationship(
            GroceryListElement,
            backref="grocery_list",
            order_by=groceries.c.id,
            default_factory=list,
            innerjoin=True,
            lazy="immediate",
        )
    },
)
mapper_registry.map_imperatively(GroceryListElement, groceries)
