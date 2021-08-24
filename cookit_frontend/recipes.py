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




def get_recipes(query, ingredients, exclusions):
    params = {'apiKey': api_keys[0],
              "query": query,
              "includeIngredients": ingredients,
              "excludeIngredients": exclusions,
              "instructionsRequired": True,
              "addRecipeInformation": True,
              "fillIngredients": True,
              "limitLicense": True,
              "ignorePantry": True,
              "ranking": 2}

    response = requests.get(BASE_URI, params)

    # TODO: if response failed due to reached quota, switch to another api key
    if response.status_code == 200:
        return response.json()['results']

    return []
