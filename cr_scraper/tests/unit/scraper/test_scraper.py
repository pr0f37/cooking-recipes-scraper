from unittest.mock import MagicMock

from pytest import raises

from cr_scraper.scraper.exceptions import InvalidURLError, SourceNotRecognisedError
from cr_scraper.scraper.recipe_components import LidlComponents
from cr_scraper.scraper.scraper import recipe_components_factory


def test_recipe_components_factory_invalid_url():
    with raises(InvalidURLError):
        recipe_components_factory(None)


def test_recipe_components_factory_unrecognised_url():
    with raises(SourceNotRecognisedError):
        recipe_components_factory("")


def test_recipe_components_factory_nonexistent_page():
    with raises(InvalidURLError):
        recipe_components_factory("kuchnialidla.pl/something")


def test_recipe_components_factory(mocker):
    with open("cr_scraper/tests/unit/scraper/static/lidl_recipe_dump", "rb") as f:
        www = f.read()
    mocker.patch(
        "cr_scraper.scraper.scraper.get", MagicMock(return_value=MagicMock(content=www))
    )
    test_components = recipe_components_factory("https://kuchnialidla.pl")
    assert isinstance(test_components, LidlComponents) is True
