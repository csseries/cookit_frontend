from requests.api import get
from cookit_frontend.recipes import get_recipes
import cookit_frontend.recipes

#Test that get_recipes returns something
def test_return_get_recipes():
    query = ["Pasta", "Zucchini", "Eggplant", "Tomato Sauce"]
    exclusions = ["Garlic"]
    cuisine = ["Italian"]
    diet = ["Vegetarian"]
    response = get_recipes(query, exclusions, cuisine, diet)

    assert response is not None


#Test that BASE_URI is complexSearch endpoint
def test_base_uri():
    BASE_URI = cookit_frontend.recipes.BASE_URI
    assert BASE_URI == 'https://api.spoonacular.com/recipes/complexSearch'


#Test that get_recipes returns a value of type list (response.json()['results'])
def test_get_recipes_return_value():
    query = ["Pasta", "Zucchini", "Eggplant", "Tomato Sauce"]
    exclusions = ["Garlic"]
    cuisine = ["Italian"]
    diet = ["Vegetarian"]
    results = get_recipes(query, exclusions, cuisine, diet)

    assert type(results) == list


#Add test for what happens when we get Status Code =! 200
# We need to think about what happens first
