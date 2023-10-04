from pytest import raises

from cr_scraper.scraper.exceptions import InvalidURLError
from cr_scraper.scraper.scraper import recipe_components_factory


def test_recipe_components_factory():
    with raises(InvalidURLError):
        recipe_components_factory(None)
