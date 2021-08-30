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



#Add test for what happens when we get Status Code =! 200
# We need to think about what happens first

#Test that get_recipes returns a response in json format if status code is 200
