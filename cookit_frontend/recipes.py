import os
import requests


# first try to load env variable from local file
api_keys = os.getenv('SPOONACULAR_KEYS')

# try to load env variable from Heroku
if api_keys == None:
    api_keys = os.environ['SPOONACULAR_KEYS'].split(',')
else:
    api_keys = api_keys.split(',')

print('Found keys in env: ', api_keys)

url = 'https://api.spoonacular.com/recipes/complexSearch'




def get_recipes(ingredients):
    params = {'query': ingredients,
              'apiKey': api_keys[0]}
    response = requests.get(url, params)

    # TODO: if response failed due to reached quota, switch to another api key
    if response.status_code == 200:
        return response.json()['results']

    return None
