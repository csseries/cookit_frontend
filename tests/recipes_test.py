from cookit_frontend.recipes import get_recipes


def test_return_get_recipes():
    query = ["Pasta", "Zucchini", "Eggplant", "Tomato Sauce"]
    ingredients = ["Basil"]
    exclusions = ["Garlic"]
    response = get_recipes(query, ingredients, exclusions)

    assert response is not None
