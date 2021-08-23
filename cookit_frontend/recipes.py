import os
import requests


api_keys = os.getenv('SPOONACULAR_KEYS').split(',')

url = 'https://api.spoonacular.com/recipes/complexSearch'




def get_recipes(ingredients):
    params = {'query': ingredients,
              'apiKey': api_keys[0]}
    response = requests.get(url, params).json()

    # TODO: if response failed due to reached quota, switch to another api key

    return response['results']
