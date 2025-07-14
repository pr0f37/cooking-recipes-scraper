# flake8: noqa
# %%
from typing import List, Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# %%
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/cr-scraper", echo=True
)
# %%

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)
metadata_obj.drop_all(engine)
# %%


class Base(DeclarativeBase):
    pass


# %%
Base.metadata

# %%
Base.registry


# %%
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}), name={self.name!r}, fullname={self.fullname!r}"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# %%
Base.metadata.create_all(engine)

# %%
metadata_obj = MetaData()

some_table = Table("some_table", metadata_obj, autoload_with=engine)

# %%
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session

from cr_scraper.grocery_list.model import GroceryList, GroceryListElement, Unit
from cr_scraper.persistence.mapper import mapper_registry
from cr_scraper.persistence.model import metadata_obj

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/cr-scraper", echo=True
)

metadata_obj.create_all(engine, checkfirst=True)

grocery = GroceryListElement(name="test_name", quantity=1.02, unit=Unit.KG)
grocery_list = GroceryList(name="test list")
grocery_list.add_element(grocery)
grocery_list.add_element(grocery)
with Session(engine) as session:
    session.add(grocery_list)
    session.commit()

# %%
## this sample assumes that db has been migrated to the latest stage

from cr_scraper.grocery_list.model import GroceryList, GroceryListElement
from cr_scraper.persistence.repository import SQLRepository

with SQLRepository() as repo:
    all_grocery_lists = repo.get_all(GroceryList)
    groceries = repo.get_all(GroceryListElement)

for g_list in all_grocery_lists:  # type: ignore
    print(g_list)

for g in groceries:  # type: ignore
    print(g)

# %%
