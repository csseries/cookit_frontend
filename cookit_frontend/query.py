import psycopg2
import os
import pandas as pd


basics = [
    "salt", "pepper", "herbs", "water", "milk", "pasta", "rice", "flour",
    "olive oil", "sunflower oil", "corn starch", "sugar", "vinegar", "tea",
    "coffee", "almonds", "stock", "egg", "spices", "honey", "wine",
    "tomato paste"
]

INGREDIENTS = [
    'Acorn Squash', 'Almond flour', 'Almonds', 'Apple', 'Apricots',
    'Artichoke', 'Artichokes', 'Asparagus', 'Aspargus', 'Avacado', 'Banana',
    'Banana Peppers', 'Bananas', 'Beef', 'Beer', 'Beets', 'Bell pepper',
    'Black Beans', 'Blackberries', 'Blueberries', 'Bread', 'Broccoli',
    'Cabbage', 'Cantaloupe', 'Carrot', 'Cauliflower', 'Cayenne pepper',
    'Celeriac', 'Celery', 'Cheese', 'Cherries', 'Chili', 'Chocolate',
    'Coconut', 'Collards', 'Corn', 'Corn stach', 'Cranberries',
    'Cranberry Beans', 'Cream', 'Cucumber', 'Egg', 'Eggplant', 'Figs', 'Fish',
    'Flour', 'Garlic', 'Ginger', 'Grape', 'Grapefruit', 'Grapes',
    'Green Asparagus', 'Green Beans', 'Guava', 'Haddock', 'Ham', 'Hazelnuts',
    'Honeydew', 'Joghurt', 'Kale', 'Kidney Beans', 'Kumquats', 'Lamb', 'Leeks',
    'Lemon', 'Lemons', 'Lentils', 'Lettuce', 'Limes', 'Mango', 'Meat',
    'Mushroom', 'Mushrooms', 'Navy Beans', 'Oats', 'Okra', 'Olive oil',
    'Onion', 'Orange', 'Oranges', 'Papaya', 'Parsnips', 'Pasta', 'Peaches',
    'Peanut Butter', 'Pear', 'Peas', 'Pecans', 'Pepper', 'Pineapple',
    'Pinto Beans', 'Pomegranate', 'Pork', 'Potato', 'Potatoes, Red',
    'Potatoes, Russet', 'Pumpkin', 'Pumpkin Seeds', 'Quinoa', 'Radish',
    'Raspberries', 'Rhubarb', 'Rice', 'Rice flour', 'Rutabagas', 'Salad',
    'Salmon', 'Salt', 'Seabass', 'Seabream', 'Serrano Pepper', 'Sesame Seeds',
    'Sesame oil', 'Shallots', 'Soya sauce', 'Soybeans', 'Spaghetti Squash',
    'Spinach', 'Squash', 'Strawberries', 'Strawberry', 'Sugar Snap Peas',
    'Summer Squash', 'Sunflower Seeds', 'Sunflower oil', 'Sweet Green Pepper',
    'Sweet Potato', 'Sweet Red Peppers', 'Sweet Yellow Peppers', 'Swiss Chard',
    'Tangerines', 'Tomato', 'Tomatoes', 'Truit', 'Turnips', 'Veal', 'Walnuts',
    'Watermelon', 'Yams', 'Zucchini'
]



def import_data():
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

    recipes = import_data()

    ingredients_joined = []

    for row in recipes.ingredients:
        ingredients_joined.append(" ".join(row))

    recipes["ingredients_joined"] = ingredients_joined

    recipes["ingredients_joined"] = recipes["ingredients_joined"].apply(str.lower)


    return recipes


def query_recipes(params_dict):

    recipes = processing_recipes()

    queried_results_list = []

    for index, row in recipes.iterrows():

        include_condition = all(x in recipes.ingredients_joined[index] for x in params_dict["includeIngredients"])
        exclude_condition = any(x in recipes.ingredients_joined[index] for x in params_dict["excludeIngredients"])
        #difficulty_condition = recipes.difficulty[index] == params["difficulty"]

        if (include_condition) and not (exclude_condition):
            queried_results_list.append(row)


    return queried_results_list


def missing_function(params_dict):
    queried_results_list = query_recipes(params_dict)
    ingr_needed = [queried_results_list[0]["ingredients_joined"]]
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


def transform_for_frontend(params_dict):
    queried_results_list = query_recipes(params_dict)

    formated_dict_list = []

    for ser in queried_results_list:
        formated_dict = {
            "image": ser["picture_url"],
            "sourceUrl": ser["link"],
            "title": ser["title"],
            "readyInMinutes": ser["preptime"],
            "missedIngredientCount": 0,
            "missedIngredients": missing_function(params_dict),
            #"missedIngredients": "not",
            "cuisine": ser["cuisine"],
            "difficulty": ser["difficulty"],
            "instructions": ser["instructions"],
            "calories": ser["calories"],
            "ingredients": ser["ingredients"]
        }

        formated_dict_list.append(formated_dict)


    return formated_dict_list
