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


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
