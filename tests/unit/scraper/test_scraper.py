from http import HTTPStatus
from unittest.mock import MagicMock

from pytest import raises

from cr_scraper.grocery_list.model import Unit
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
        recipe_components_factory(1)


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
    assert [
        (name, quantity, unit)
        for name, quantity, unit in test_components.get_ingredients()
    ] == [
        ("ingredient_1.1", 11.0, Unit.MG),
        ("ingredient_1.2", 12.0, Unit.G),
        ("ingredient_2.1", 21.0, Unit.KG),
        ("ingredient_2.2", 22.0, Unit.ML),
        ("ingredient_2.3", 23.0, Unit.L),
    ]
