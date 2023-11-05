from sqlalchemy import UUID, Column, Enum, Float, ForeignKey, MetaData, String, Table

from cr_scraper.grocery_list.model import Unit

metadata_obj = MetaData()

unit_enum = Enum(Unit, create_constraint=True, metadata=metadata_obj, native_enum=True)

grocery_lists = Table(
    "grocery_lists",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
)

groceries = Table(
    "groceries",
    metadata_obj,
    Column("id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("quantity", Float, nullable=True),
    Column("unit", unit_enum, nullable=True),
    Column("list_id", UUID, ForeignKey("grocery_lists.id")),
)
