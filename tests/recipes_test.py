from requests.api import get
from cookit_frontend.recipes import get_recipes
import cookit_frontend.recipes

#Test that get_recipes returns something
def test_return_get_recipes():
    query = ["Pasta", "Zucchini", "Eggplant", "Tomato Sauce"]
    ingredients = ["Basil"]
    exclusions = ["Garlic"]
    response = get_recipes(query, ingredients, exclusions)

    assert response is not None


#Test that BASE_URI is complexSearch endpoint
def test_base_uri():
    BASE_URI = cookit_frontend.recipes.BASE_URI
    assert BASE_URI == 'https://api.spoonacular.com/recipes/complexSearch'


#Test that get_recipes returns a value of type list (response.json()['results'])
def test_get_recipes_return_value():
    query = ["Pasta", "Zucchini", "Eggplant", "Tomato Sauce"]
    ingredients = ["Basil"]
    exclusions = ["Garlic"]
    results = get_recipes(query, ingredients, exclusions)

    assert type(results) == list

#Test that status code == 200
#Hard-coded sample query with API key. DO NOT USE publicly on Github
def test_get_recipes_sample_query_status_code_equals_200():
    response = get(
        "https://api.spoonacular.com/recipes/complexSearch?apiKey=740a5cf41e434eb1b27f2622646c9107&query=pasta&includeIngredients=tomato&excludeIngredients=tuna")
    assert response.status_code == 200

#Add test for what happens when we get Status Code =! 200
# We need to think about what happens first
