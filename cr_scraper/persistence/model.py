from sqlalchemy import Column, Float, Integer, MetaData, String, Table

metadata_obj = MetaData()


groceries = Table(
    "groceries",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("quantity", Float, nullable=True),
    Column("unit", String, nullable=True),
)
