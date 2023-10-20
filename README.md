# Welcome to Cooking Recipes Scraper

The purpose of this application is to enable scraping the web pages containing recipes to obtain a list of cooking ingredients. Cooking ingredients then are grouped, added and combined into a common grocery shopping list.

## Documentation
Additional project documentation available [here](/docs/index.md)

## Local setup
### Docker
Run in docker using the docker compose
```bash
$ docker-compose up
```
And you should be good to go. Application will be running on `0.0.0.0:8000`
### Virtual environment
Application requires python `3.11`
Set up local environment with `pyenv` and `pip`
```bash
$ pyenv virtualenv 3.11.5 cr-scraper
$ pyenv shell cr-scraper
$ pip install -r requirements.txt
$ pip install .
```
#### Running the application
After setting up the virtual environment run the app with
```bash
$ uvicorn 'cr_scraper.main:app' --host=0.0.0.0 --port=8000
```
Application will be running on `0.0.0.0:8000`

## License
This software is released under the [MIT license](/LICENSE).
