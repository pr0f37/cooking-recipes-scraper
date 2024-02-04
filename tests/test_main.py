from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import HttpUrl

from cr_scraper.api.main import app
from cr_scraper.grocery_list.model import GroceryList, GroceryListElement
from cr_scraper.persistence.repository import NotExistInRepositoryError
from cr_scraper.scraper.model import Ingredient, Recipe

client = TestClient(app)
test_url = "https://test_url.com"
http_test_url = f"{HttpUrl(test_url)}"
list_uuid = uuid4()
grocery_list = GroceryList(
    groceries=[GroceryListElement(name="test_name", quantity=1.0, unit="kg")],
    id=list_uuid,
    name="test_name",
)


def test_scrape_recipe(mocker):
    scrape_recipe_mock = mocker.patch(
        "cr_scraper.api.router.api.scrape_recipe",
        return_value=Recipe(
            url=http_test_url,
            difficulty="*",
            title="test_recipe_title",
            time="5 minutes",
            ingredients=[Ingredient(name="test_ingredient", quantity=1.0, unit="kg")],
        ),
    )
    response = client.post("/api/recipes/scrape", json={"url": test_url})
    scrape_recipe_mock.assert_called_with(http_test_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "url": http_test_url,
        "ingredients": [{"name": "test_ingredient", "quantity": 1.0, "unit": "kg"}],
        "title": "test_recipe_title",
        "time": "5 minutes",
        "difficulty": "*",
    }


@pytest.mark.parametrize(
    ("url", "type", "msg"),
    [
        (None, "url_type", "URL input should be a string or URL"),
        ("htp://www.www.www", "url_scheme", "URL scheme should be 'http' or 'https'"),
        ("https://", "url_parsing", "Input should be a valid URL, empty host"),
        (
            "www.test.com",
            "url_parsing",
            "Input should be a valid URL, relative URL without a base",
        ),
    ],
)
def test_scrape_recipe_errors(mocker, url, type, msg):
    scrape_recipe_mock = mocker.patch("cr_scraper.api.router.api.scrape_recipe")
    response = client.post("/api/recipes/scrape", json={"url": url})
    assert response.json()["detail"][0]["type"] == type
    assert response.json()["detail"][0]["loc"] == ["body", "url"]
    assert response.json()["detail"][0]["msg"] == msg
    assert response.json()["detail"][0]["input"] == url
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    scrape_recipe_mock.assert_not_called()


def test_display_all_grocery_lists(mocker):
    mocker.patch(
        "cr_scraper.api.router.api.get_all_grocery_lists",
        return_value=[grocery_list],
    )
    response = client.get("/api/grocery_lists")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "id": f"{list_uuid}",
            "name": "test_name",
            "groceries": [{"name": "test_name", "quantity": 1.0, "unit": "kg"}],
        }
    ]


def test_display_all_grocery_lists_empty_groceries(mocker):
    mocker.patch(
        "cr_scraper.api.router.api.get_all_grocery_lists",
        return_value=[
            GroceryList(
                groceries=[],
                id=list_uuid,
                name="test_name",
            )
        ],
    )
    response = client.get("/api/grocery_lists")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "id": f"{list_uuid}",
            "name": "test_name",
            "groceries": [],
        }
    ]


def test_display_all_grocery_lists_empty_lists(mocker):
    mocker.patch(
        "cr_scraper.api.router.api.get_all_grocery_lists",
        return_value=[],
    )
    response = client.get("/api/grocery_lists")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_add_recipe_to_groceries_list(mocker):
    update_list_mock = mocker.patch(
        "cr_scraper.api.router.api.update_list_add_recipe", return_value=grocery_list
    )
    response = client.post(
        f"/api/grocery_lists/{list_uuid}/add_recipe", json={"url": test_url}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": f"{list_uuid}",
        "name": "test_name",
        "groceries": [{"name": "test_name", "quantity": 1.0, "unit": "kg"}],
    }
    update_list_mock.assert_called_with(http_test_url, list_uuid)


def test_add_recipe_to_groceries_list_error(mocker):
    update_list_mock = mocker.patch(
        "cr_scraper.api.router.api.update_list_add_recipe",
        side_effect=NotExistInRepositoryError,
    )
    response = client.post(
        f"/api/grocery_lists/{list_uuid}/add_recipe", json={"url": test_url}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": f"Grocery list {list_uuid} not exists"}
    update_list_mock.assert_called_with(http_test_url, list_uuid)


@pytest.mark.parametrize(
    ("url", "type", "msg"),
    [
        (None, "url_type", "URL input should be a string or URL"),
        ("htp://www.www.www", "url_scheme", "URL scheme should be 'http' or 'https'"),
        ("https://", "url_parsing", "Input should be a valid URL, empty host"),
        (
            "www.test.com",
            "url_parsing",
            "Input should be a valid URL, relative URL without a base",
        ),
    ],
)
def test_add_recipe_to_groceries_list_marshalling_error(mocker, url, type, msg):
    update_list_mock = mocker.patch(
        "cr_scraper.api.router.api.update_list_add_recipe",
        side_effect=NotExistInRepositoryError,
    )
    response = client.post(
        f"/api/grocery_lists/{list_uuid}/add_recipe", json={"url": url}
    )
    assert response.json()["detail"][0]["type"] == type
    assert response.json()["detail"][0]["loc"] == ["body", "url"]
    assert response.json()["detail"][0]["msg"] == msg
    assert response.json()["detail"][0]["input"] == url
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    update_list_mock.assert_not_called()
