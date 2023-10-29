from http import HTTPStatus
from unittest.mock import MagicMock

from pytest import raises

from cr_scraper.scraper.exceptions import (
    HTTPWebPageError,
    InvalidURLError,
    SourceNotRecognisedError,
)
from cr_scraper.scraper.recipe_components import LidlComponents
from cr_scraper.scraper.scraper import recipe_components_factory

with open("tests/unit/scraper/static/lidl_recipe_dump", "rb") as f:
    WEB_CONTENT = f.read()


def test_recipe_components_factory_invalid_url():
    with raises(InvalidURLError):
        recipe_components_factory(None)


def test_recipe_components_factory_unrecognised_url():
    with raises(SourceNotRecognisedError):
        recipe_components_factory("")


def test_recipe_components_factory_nonexistent_page():
    with raises(InvalidURLError):
        recipe_components_factory("kuchnialidla.pl/something")


def test_recipe_components_factory_http_not_OK(mocker):
    mocker.patch(
        "cr_scraper.scraper.scraper.get",
        MagicMock(
            return_value=MagicMock(
                content=WEB_CONTENT,
                status_code=HTTPStatus.CONFLICT,
            )
        ),
    )
    with raises(HTTPWebPageError):
        recipe_components_factory("https://kuchnialidla.pl")


def test_lidl_components(mocker):
    mocker.patch(
        "cr_scraper.scraper.scraper.get",
        MagicMock(
            return_value=MagicMock(
                content=WEB_CONTENT,
                status_code=HTTPStatus.OK,
            )
        ),
    )
    test_components = recipe_components_factory("https://kuchnialidla.pl")
    assert isinstance(test_components, LidlComponents) is True
    assert test_components.get_title() == "test_title"
    assert test_components.get_ingredients() == [
        "ingredient_1.1",
        "ingredient_1.2",
        "ingredient_2.1",
        "ingredient_2.2",
        "ingredient_2.3",
    ]
