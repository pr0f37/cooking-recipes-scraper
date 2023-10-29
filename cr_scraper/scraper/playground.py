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
details.h1.text
# %%
skladniki = details.find("div", class_="skladniki")

# %%
[li.text for li in skladniki.find_all("li")]

# %%
host = "https://kuchnialidla.pl"
r = requests.get(f"{host}/przepisy")
soup = BeautifulSoup(r.content, "html.parser")

# %%
recipes = soup.find_all("a", class_="description")
recipes
# %%
parsed_recipes = []
for recipe in recipes:
    recipe_html = requests.get(f"{host}{recipe['href']}")
    recipe_soup = BeautifulSoup(recipe_html.content, "html.parser")
    recipe_details = recipe_soup.find("div", id="details")
    recipe_title = recipe_details.h1.text
    recipe_ingredients = recipe_details.find("div", class_="skladniki")
    recipe_ingredients_text = [li.text for li in recipe_ingredients.find_all("li")]
    parsed_recipes.append(
        {"title": recipe_title, "ingredients": recipe_ingredients_text}
    )


# %%

print(json.dumps(parsed_recipes))

# %%
len(recipes) == len(parsed_recipes)
# %%
