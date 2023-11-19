from uuid import UUID

from pydantic import BaseModel, HttpUrl


class Url(BaseModel):
    url: HttpUrl


class UrlAndTitle(Url):
    title: str


class GroceryListElementResponse(BaseModel):
    name: str
    quantity: float
    unit: str


class GroceryListResponse(BaseModel):
    id: UUID
    name: str
    groceries: list[GroceryListElementResponse]
