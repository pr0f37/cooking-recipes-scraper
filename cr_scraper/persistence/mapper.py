from sqlalchemy.orm import registry

from cr_scraper.grocery_list.model import GroceryListElement
from cr_scraper.persistence.model import groceries

mapper_registry = registry()

mapper_registry.map_imperatively(GroceryListElement, groceries)
