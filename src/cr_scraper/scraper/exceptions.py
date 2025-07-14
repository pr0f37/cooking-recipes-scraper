class ScraperError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidURLError(ScraperError):
    def __init__(self, url: str, *args: object) -> None:
        self.msg = f"The web page url address is invalid: {url}"
        super().__init__(self.msg, *args)


class SourceNotRecognisedError(ScraperError):
    def __init__(self, *args: object) -> None:
        self.msg = (
            "Page containing the resource is not scrapable. Try different web page"
        )
        super().__init__(self.msg, *args)


class HTTPWebPageError(ScraperError):
    def __init__(self, url: str, status_code: int, *args: object) -> None:
        self.msg = f"The web page: {url} returned unexpected status code: {status_code}"
        super().__init__(self.msg, *args)
