from sqlalchemy import UUID, Column, Float, ForeignKey, MetaData, String, Table

metadata_obj = MetaData()

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
    Column("unit", String, nullable=True),
    Column("list_id", UUID, ForeignKey("grocery_lists.id")),
)
