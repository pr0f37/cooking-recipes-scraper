from fastapi.testclient import TestClient
from pydantic import HttpUrl

from cr_scraper.api.main import app
from cr_scraper.scraper.model import Ingredient, Recipe

client = TestClient(app)


def test_scrape_recipe(mocker):
    test_url = "https://test_url.com"
    http_test_url = f"{HttpUrl(test_url)}"
    scrape_recipe_mock = mocker.patch(
        "cr_scraper.api.main.scrape_recipe",
        return_value=Recipe(
            url=http_test_url,
            difficulty="*",
            title="test_recipe_title",
            time="5 minutes",
            ingredients=[Ingredient(name="test_ingredient", quantity=1.0, unit="kg")],
        ),
    )
    response = client.post("/recipes/scrape", json={"url": test_url})
    scrape_recipe_mock.assert_called_with(http_test_url)
    assert response.status_code == 200
    assert response.json() == {
        "url": http_test_url,
        "ingredients": [{"name": "test_ingredient", "quantity": 1.0, "unit": "kg"}],
        "title": "test_recipe_title",
        "time": "5 minutes",
        "difficulty": "*",
    }
