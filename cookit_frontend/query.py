import psycopg2
import os
import pandas as pd
from cookit_frontend.utils import BASICS



def import_data():
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


def query_recipes(params_dict):
    # query the database  and return a list of series (containing the information regarding the recipes)
    recipes = processing_recipes()

    queried_results_list = []

    # lowercase the input from the frontend
    for key in params_dict:
        if type(params_dict[key]) == type([]):
            for index, item in enumerate(params_dict[key]):
                params_dict[key][index] = item.lower()

    # query the database recipe df based on conditions
    for index, row in recipes.iterrows():

        include_condition = all(x in recipes.ingredients_joined[index] for x in params_dict["includeIngredients"])
        exclude_condition = any(x in recipes.ingredients_joined[index] for x in params_dict["excludeIngredients"])
        #difficulty_condition = recipes.difficulty[index] == params_dict["difficulty"]

        if (include_condition) and not (exclude_condition):
            queried_results_list.append(row)


    return queried_results_list


def missing_function(params_dict, index):
    # This function does now work properly -- Still want to rewrite?
    queried_results_list = query_recipes(params_dict)
    ingr_needed = [queried_results_list[index]["ingredients_joined"]]
    ingr_available = params_dict["includeIngredients"] + basics

    ingr_needed = " ".join(ingr_needed).split(" ")

    for ingr in ingr_available:
        for index, string in enumerate(ingr_needed):
            if ingr in string:
                del ingr_needed[index]

    ingr_needed_striped = []

    for i in ingr_needed:
        i = i.strip(",")
        ingr_needed_striped.append(i)

    ingredients_list = []

    for i in INGREDIENTS:
        i = i.lower()
        ingredients_list.append(i)

    return_frontend_list = []

    for i in ingr_needed_striped:
        if i in ingredients_list:
            return_frontend_list.append(i)


    return return_frontend_list


def find_recipes_in_db(ingredients, exclusions, difficulty):
    params_dict = {
        "includeIngredients": [i.lower() for i in ingredients],
        "excludeIngredients": [i.lower() for i in exclusions],
        "difficulty": difficulty.lower()
    }
    # Return a list of dictionaries containing information regarding recipes
    queried_results_list = query_recipes(params_dict)

    formated_dict_list = []

    for index, ser in enumerate(queried_results_list):
        formated_dict = {
            "image": ser["picture_url"],
            "sourceUrl": ser["link"],
            "title": ser["title"],
            "readyInMinutes": ser["preptime"],
            "missedIngredientCount": 0,
            "missedIngredients": missing_function(params_dict, index),
            #"missedIngredients": "not",
            "cuisine": ser["cuisine"],
            "difficulty": ser["difficulty"],
            "instructions": ser["instructions"],
            "calories": ser["calories"],
            "ingredients": ser["ingredients"]
        }

        formated_dict_list.append(formated_dict)


    return formated_dict_list
