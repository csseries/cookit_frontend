import os
import requests
import random

# load env variable from Heroku or from local environment
try:
    api_keys = os.environ['SPOONACULAR_KEYS'].split(',')
    print('Found keys in env: ', api_keys)
except:
    api_keys = []
    print('WARNING: No spoonacular API keys found in environment!')


BASE_URI = 'https://api.spoonacular.com/recipes/complexSearch'

KEY_IDX = 0 # initial value for api keys



def get_recipes(ingredients, exclusions, cuisine, diet):
    global KEY_IDX
    print(f"Using API key index: {KEY_IDX}")

    offset = random.randint(0, 20)
    # See https://spoonacular.com/food-api/docs#Search-Recipes-Complex
    params = {'apiKey': api_keys[KEY_IDX],
              #The (natural language) recipe search query
              #"query": query,
              #A comma-separated list of ingredients that should/must be used in the recipes
              "includeIngredients": ingredients,
              #A comma-separated list of ingredients or ingredient types that the recipes must not contain
              "excludeIngredients": exclusions,
              #The cuisine(s) of the recipes. One or more, comma separated (will be interpreted as 'OR')
              "cuisine": cuisine,
              #The diet for which the recipes must be suitable
              "diet": diet,
              #Only recipes with instructions
              "instructionsRequired": True,
              "addRecipeInformation": True,
              #Add information about the ingredients and whether they are used or missing in relation to the query
              "fillIngredients": True,
              "ignorePantry": True,
              #Other option is max-used-ingredients
              "sort": "min-missing-ingredients",
              #The direction in which to sort. Must be either 'asc' (ascending) or 'desc' (descending)
              "sortDirection": "asc",
              #Number of expected results (between 1 and 100)


              "number": 3,
              # The number of results to skip (between 0 and 900).
              # This is a bit risky in cases where less recipes were found than the offset value;
              # --> the API is then returning no recipes.

              "offset": offset}

    response = requests.get(BASE_URI, params)
    print(params)

    if response.status_code == 200:
        return response.json()['results']

    # if response failed due to reached quota, switch to another api key
    if response.status_code == 402:
        print("Daily quota is reachend - switch to next API key in list")
        KEY_IDX = (KEY_IDX + 1) % len(api_keys)
        get_recipes(ingredients, exclusions, cuisine, diet)
    return []
