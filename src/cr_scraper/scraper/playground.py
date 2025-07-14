# flake8: noqa
# %%
import json

import requests
from bs4 import BeautifulSoup

r = requests.get("https://kuchnialidla.pl/wege-placki-z-tartych-warzyw")
soup = BeautifulSoup(r.content, "html.parser")

# print(soup.prettify())

# %%
details = soup.find("div", id="details")

# %%
details.h1.text  # type: ignore
# %%
skladniki = details.find("div", class_="skladniki")  # type: ignore

# %%
[li.text for li in skladniki.find_all("li")]  # type: ignore

# %%
host = "https://kuchnialidla.pl"
r = requests.get(f"{host}/przepisy")
soup = BeautifulSoup(r.content, "html.parser")

# %%
recipes = soup.find_all("a", class_="description")
# %%
parsed_recipes = []
for recipe in recipes:
    recipe_html = requests.get(f"{host}{recipe['href']}")
    recipe_soup = BeautifulSoup(recipe_html.content, "html.parser")
    recipe_details = recipe_soup.find("div", id="details")
    recipe_title = recipe_details.h1.text  # type: ignore
    recipe_ingredients = recipe_details.find("div", class_="skladniki")  # type: ignore
    recipe_ingredients_text = [li.text for li in recipe_ingredients.find_all("li")]  # type: ignore
    parsed_recipes.append(
        {"title": recipe_title, "ingredients": recipe_ingredients_text}
    )


# %%

print(json.dumps(parsed_recipes))
