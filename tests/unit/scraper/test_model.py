from pytest import raises

from cr_scraper.scraper.exceptions import SourceNotRecognisedError
from cr_scraper.scraper.model import Ingredient, Recipe, RecipesSource


def test_source_not_recognised():
    with raises(SourceNotRecognisedError) as ex_info:
        RecipesSource.which_source("test")
    assert (
        ex_info.value.msg
        == "Page containing the resource is not scrapable. Try different web page"
    )


def test_source_recognised():
    test_source = RecipesSource.which_source("kuchnialidla.pl")
    assert test_source is RecipesSource.LIDL


def test_source_recognised_uppercase():
    test_source = RecipesSource.which_source("KUCHNIALIDLA.PL")
    assert test_source is RecipesSource.LIDL


def test_source_recognised_longer_url():
    test_source = RecipesSource.which_source("https://KUCHNIALIDLA.PL/przepisy")
    assert test_source is RecipesSource.LIDL


def test_recipe_class_mandatory_elements():
    recipe = Recipe(
        url="test_url",
        ingredients=[
            Ingredient("ingredient1", 1, "handful"),
            Ingredient("ingredient2", 2, "test"),
        ],
        title="test_title",
    )
    assert recipe is not None
