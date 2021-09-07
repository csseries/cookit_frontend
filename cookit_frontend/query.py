import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection
import os
import streamlit as st
from cookit_frontend.utils import BASICS


## Schema of DB
#    CREATE TABLE COOKIT_RECIPES
#    (ID INT PRIMARY KEY     NOT NULL,
#    TITLE           TEXT    NOT NULL,
#    DIFFICULTY      TEXT,
#    PREPTIME        INT,
#    NUMBER_OF_INGREDIENTS INT,
#    INGREDIENTS     TEXT[]     NOT NULL,
#    CUISINE         TEXT     NOT NULL,
#    CALORIES        TEXT,
#    LINK            TEXT       NOT NULL,
#    PICTURE_URL     TEXT       NOT NULL,
#    INSTRUCTIONS    TEXT);


try:
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_USER = os.environ['DB_USER']
    DB_HOST = os.environ['DB_HOST']
except:
    print("ERROR: Couldn't find all requested env variables for DB connection!")



# Caches the connection and avoids a re-connection every time the user changes something
# Seen in https://discuss.streamlit.io/t/prediction-analysis-and-creating-a-database/3504
@st.cache(hash_funcs={connection: id})
def open_db_connection():
    conn = psycopg2.connect(database="d1hsr1c7nk56dl",
                            user=DB_USER,
                            host=DB_HOST,
                            port="5432",
                            password=DB_PASSWORD)
    print("Connection established")
    return conn


def query_recipes(conn, include_ingredients, exclude_ingredients):
    # Add wildcard operators to list elements
    include_ingredients = [f"%{x}%" for x in include_ingredients]
    exclude_ingredients = [f"%{x}%" for x in exclude_ingredients]

    # RealDictCursor enables us to access the fetched rows in dict style like recipes['ingredients']
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # the ILIKE makes sure we are searching case-insensitive
    # there may be other possibilities, but making a string of the array and search for all given
    # ingredients is the most straightforward approach so far
    query = """
        SELECT ID, TITLE, PREPTIME, INGREDIENTS, CUISINE, LINK, PICTURE_URL, DIFFICULTY
        FROM cookit_recipes
        WHERE ARRAY_TO_STRING(cookit_recipes.INGREDIENTS, ',') ILIKE ALL (%(include_ingredients)s)
        AND NOT
        ARRAY_TO_STRING(cookit_recipes.INGREDIENTS, ',') ILIKE ANY (%(exclude_ingredients)s)
    """
    cur.execute(query, {'include_ingredients': include_ingredients,
                        'exclude_ingredients': exclude_ingredients})
    return cur.fetchall()


def get_missing_ingredients(recipe_ingredients, ingredients):
    available_list = []
    for ingr in ingredients + BASICS:
        available_list += [
            x for x in recipe_ingredients if ingr.lower() in x.lower()
        ]
    missing = list(set(recipe_ingredients) - set(available_list))

    return missing

def find_recipes_in_db(conn, ingredients, exclusions):
    """ Return a list of dictionaries containing information regarding recipes """
    queried_results_list = query_recipes(conn, ingredients, exclusions)

    formated_dict_list = []
    for recipe in queried_results_list:
        missing_ingredients = get_missing_ingredients(recipe['ingredients'], ingredients)
        formated_dict = {
            "image": recipe["picture_url"],
            "sourceUrl": recipe["link"],
            "title": recipe["title"],
            "readyInMinutes": recipe["preptime"],
            "missedIngredientCount": len(missing_ingredients),
            "missedIngredients": missing_ingredients,
            "cuisine": recipe["cuisine"],
            "difficulty": recipe["difficulty"],
            "ingredients": recipe["ingredients"]
        }
        formated_dict_list.append(formated_dict)

    # sort by missing ingredients ascending
    resorted_list = sorted(formated_dict_list, key=lambda k: k['missedIngredientCount'])
    return resorted_list
