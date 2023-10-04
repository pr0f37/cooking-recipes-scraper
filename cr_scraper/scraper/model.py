from dataclasses import dataclass
from enum import Enum

from cr_scraper.scraper.exceptions import InvalidURLError, SourceNotRecognisedError


@dataclass
class Recipe:
    url: str
    ingredients: list[str]
    title: str
    time: None | str = None
    difficulty: None | str = None


class RecipesSource(Enum):
    LIDL = "kuchnialidla.pl"

    @classmethod
    def which_source(cls, url: str):
        try:
            if cls.LIDL.value in url.lower():
                return cls.LIDL
        except AttributeError:
            raise InvalidURLError(url)
        raise SourceNotRecognisedError()
