import psycopg2
import os
import pandas as pd
from cookit_frontend.utils import BASICS



def import_data():
    print("IMPORT DATA FROM DB")
    # Connection to database and return an DataFrame called recipes
    DB_PASSWORD = os.environ['DB_PASSWORD']

    conn = psycopg2.connect(database="d1hsr1c7nk56dl",
                            user="iadkkqrgljveni",
                            host="ec2-3-230-61-252.compute-1.amazonaws.com",
                            port="5432",
                            password=DB_PASSWORD)

    query = """
    SELECT *
    FROM cookit_recipes
    """
    recipes = pd.read_sql(query, conn)
    print("DONE WITH IMPORTING DATA FROM DB")

    return recipes


def processing_recipes():
    # Add "ingredients_joined" to recipes df in order to query the recipes
    recipes = import_data()

    ingredients_joined = []
    for row in recipes.ingredients:
        ingredients_joined.append(" ".join(row))

    recipes["ingredients_joined"] = ingredients_joined
    recipes["ingredients_joined"] = recipes["ingredients_joined"].apply(str.lower)

    return recipes

# Storing the database here in a global variable is not very elegant, but workaround for the moment.
recipes = processing_recipes()

def query_recipes(params_dict):
    # query the database  and return a list of series (containing the information regarding the recipes)
    global recipes

    queried_results_list = []
    # TODO: There should be a faster way to get the results from the dataframe
    for index, row in recipes.iterrows():
        include_condition = all(x in recipes.ingredients_joined[index] for x in params_dict["includeIngredients"])
        exclude_condition = any(x in recipes.ingredients_joined[index] for x in params_dict["excludeIngredients"])
        #difficulty_condition = recipes.difficulty[index] == params_dict["difficulty"]

        #if include_condition and not exclude_condition and difficulty_condition:
        if include_condition and not exclude_condition:
            queried_results_list.append(row)

    return queried_results_list


def get_missing_ingredients(recipe_ingredients, ingredients):
    available_list = []
    for ingr in ingredients + BASICS:
        available_list += [x for x in recipe_ingredients if ingr in x]
    missing = list(set(recipe_ingredients) - set(available_list))

    return missing


def find_recipes_in_db(ingredients, exclusions):
    params_dict = {
        "includeIngredients": [i.lower() for i in ingredients],
        "excludeIngredients": [i.lower() for i in exclusions],
        #"difficulty": difficulty.lower()
    }
    # Return a list of dictionaries containing information regarding recipes
    queried_results_list = query_recipes(params_dict)

    formated_dict_list = []

    for recipe in queried_results_list:
        missing_ingredients = get_missing_ingredients(recipe['ingredients'], params_dict['includeIngredients'])
        formated_dict = {
            "image": recipe["picture_url"],
            "sourceUrl": recipe["link"],
            "title": recipe["title"],
            "readyInMinutes": recipe["preptime"],
            "missedIngredientCount": len(missing_ingredients),
            "missedIngredients": missing_ingredients,
            "cuisine": recipe["cuisine"],
            "difficulty": recipe["difficulty"],
            "instructions": recipe["instructions"],
            "calories": recipe["calories"],
            "ingredients": recipe["ingredients"]
        }

        formated_dict_list.append(formated_dict)

    # sort by missing ingredients ascending
    resorted_list = sorted(formated_dict_list, key=lambda k: k['missedIngredientCount'])

    return resorted_list
