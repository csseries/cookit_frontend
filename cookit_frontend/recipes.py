import os
import requests


# load env variable from Heroku or from local environment
try:
    api_keys = os.environ['SPOONACULAR_KEYS'].split(',')
    print('Found keys in env: ', api_keys)
except:
    api_keys = []
    print('WARNING: No spoonacular API keys found in environment!')


BASE_URI = 'https://api.spoonacular.com/recipes/complexSearch'




def get_recipes(query, ingredients, exclusions, cuisine):
    params = {'apiKey': api_keys[0],
              #The (natural language) recipe search query
              "query": query,
              #A comma-separated list of ingredients that should/must be used in the recipes
              "includeIngredients": ingredients,
              #A comma-separated list of ingredients or ingredient types that the recipes must not contain
              "excludeIngredients": exclusions,
              #The cuisine(s) of the recipes. One or more, comma separated (will be interpreted as 'OR')
              "cuisine": cuisine,
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
              "number": 15}

    response = requests.get(BASE_URI, params)
    print(params)

    # TODO: if response failed due to reached quota, switch to another api key
    if response.status_code == 200:
        return response.json()['results']

    return []
