# Welcome to Cooking Recipes Scraper

The purpose of this application is to enable scraping the web pages containing recipes to obtain a list of cooking ingredients. Cooking ingredients then are grouped, added and combined into a grocery shopping list.

- [Documentation](#documentation)
- [Local setup](#local-setup)
  - [Virtual environment](#virtual-environment)
  - [Running the app](#running-the-app)
    - [Manual Docker](#manual-docker)
    - [Docker-compose](#docker-compose)
    - [In a virtual environment](#in-a-virtual-environment)
  - [Testing](#testing)
    - [Manual Docker](#manual-docker-1)
    - [Docker-compose](#docker-compose-1)
    - [In a virtual environment](#in-a-virtual-environment-1)
  - [Additional tools](#additional-tools)
    - [Pre-commit](#pre-commit)
- [License](#license)

## Documentation

Additional project documentation available [here](/docs/index.md)

## Local setup

There are several methods to run your application available depending on your particular needs and available tools.

### Virtual environment

Application requires `python 3.11`

The suggested method to set up local environment is with [`pyenv`](https://github.com/pyenv/pyenv)/[`virtualenv`](https://github.com/pyenv/pyenv-virtualenv) and [`poetry`](https://python-poetry.org/):

```bash
pyenv virtualenv 3.11.5 cr-scraper
pyenv local cr-scraper
pyenv shell cr-scraper
pip install -r requirements.txt
poetry install
```

### Running the app

Application can be run directly in `venv`, `docker` or using the `docker-compose` scripts.

Running the application using the latter way sets up the whole environment with additional containers like Postgres operational database.

#### Manual Docker

To build and run manually in docker

```bash
docker build -t scraper -f docker/dev/Dockerfile .
docker run -it --rm -p 8000:8000 scraper
```

#### Docker-compose

Run in docker using the docker compose

```bash
docker-compose up -d
```

In response you should see the following:

```shell
[+] Running 3/3
 ✔ Network cooking-recipes-scraper_default     Created   0.1s
 ✔ Container cooking-recipes-scraper-db-1      Healthy   0.0s
 ✔ Container cooking-recipes-scraper-server-1  Started   0.1s
```

And you should be good to go. Application will be running on `0.0.0.0:8000`

#### In a virtual environment

After [setting up and activating the virtual environment](#virtual-environment) run the app:

```bash
uvicorn 'cr_scraper.main:app' --host=0.0.0.0 --port=8000
```

Application will be running on `0.0.0.0:8000`

### Testing

The same as running the application there are several ways to test it.

#### Manual Docker

First build the testing image:

```
docker build -t scraper_test -f docker/test/Dockerfile.test .
```

Then run the whole suite of unit-tests, code linting and formatting checks:

```bash
docker run -it --rm scraper_test [test|lint|format]
```

#### Docker-compose

Run the whole suite of unit-tests, code linting and formatting checks or the chose subset:

```bash
docker-compose -f compose.test.yaml up --build [test|lint|format]
```

#### In a virtual environment

After [setting up and activating the virtual environment](#virtual-environment) run the tests:

```bash
pytest .
```

Or check formatting:

```bash
black . --check
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

### Additional tools

#### Pre-commit

`pre-commit` can be used to automatically check and correct files before committing them.
It comes pre-installed if you follow the [local setup virtual environments](#virtual-environment) instructions, otherwise you can install it with `pip`.

To enable automatic integration with git you need to install the git hooks:

```bash
pre-commit install
# pre-commit installed at .git/hooks/pre-commit
```

After doing this every time you commit all the staged files will be automatically tested by pre-commit. If pre-commit finds any malformed code it will correct it and ask you to stage and commit the corrected files again.

For example:

```bash
$ git status

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   tests/test_main.py
no changes added to commit (use "git add" and/or "git commit -a")

$ git add .
$ git commit -m "trying to commit malformed code"

trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing tests/test_main.py

fix end of files.........................................................Passed
check for added large files..............................................Passed
black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted tests/test_main.py

All done! ✨ 🍰 ✨
1 file reformatted.

$ git status

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   tests/test_main.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   tests/test_main.py

$ git add .
$ git commit -m "commit corrected code"

trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check for added large files..............................................Passed
black....................................................................Passed
[poetry fcbad3a] commit corrected code
 1 file changed, 4 insertions(+)
```

## License

This software is released under the [MIT license](/LICENSE).
