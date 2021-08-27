import streamlit as st
import os
import base64
from PIL import Image
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions
from cookit_frontend.image import resize_image, draw_boxes, pil_to_buffer
from cookit_frontend.page_elements import *

page_decorators()

page_title()

page_slogan()

#Option to upload jpg/ png image that will be used from the model
uploaded_file = page_pic_uploader()

if uploaded_file:
    resized_file = resize_image(uploaded_file)
    ingredients, scores, bboxes = get_predictions(pil_to_buffer(resized_file))

    all_cuisines = ["African", "American", "British", "Cajun", "Caribbean",
                    "Chinese", "Eastern European", "European", "French",
                    "German", "Greek", "Indian", "Irish", "Italian", "Japanese",
                    "Jewish", "Korean", "Latin American", "Mediterranean",
                    "Mexican", "Middle Eastern", "Nordic","Southern",
                    "Spanish", "Thai", "Vietnamese"]

    dietary_resitrictions = ["I eat everything", "Gluten Free", "Ketogenic", "Vegetarian", "Lacto-Vegetarian", "Ovo-Vegetarian",
                             "Vegan", "Pescetarian", "Paleo"]

    if len(ingredients) > 0:
        bbox_image = draw_boxes(resized_file, bboxes, ingredients, scores)
        st.image(bbox_image)

        ingredients_selected = st.multiselect('Check ingredients to include in recipes', ingredients, default=ingredients)
        ingredients_selected_formatted = ", ".join(ingredients_selected)

        must_haves = st.multiselect('Add ingredients that must be included', ingredients_selected)
        must_haves_formatted = ", ".join(must_haves)

        exclusions = st.text_input("What don't you like in your food? (comma-separated)")

        #A comma-separated list of cuisines
        cuisine = st.multiselect('What cuisine would you like to cook?', all_cuisines, default=all_cuisines)
        cuisines_formatted = ", ".join(cuisine)

        #Specify a specific diet
        diet = st.selectbox("Do you have any dietary restrictions?", dietary_resitrictions)
        if diet == "I eat everything":
            diet = []

        # this is just to avoid making too many requests during development
        if st.button('get recipes'):
            recipes = get_recipes(ingredients_selected_formatted, must_haves_formatted, exclusions, cuisines_formatted, diet)

            if len(recipes) > 0:
                for i in range(min(len(recipes), 3)):
                    col1, col2 = st.columns([3,5])
                    with col1:
                        st.image(recipes[i]['image'], use_column_width=True)
                    with col2:
                        st.write(recipes[i]['title'])
                        st.write(f"Cooking time: {recipes[i]['readyInMinutes']} minutes")
                        st.write("Cook this [recipe](%s) now" % recipes[i]["sourceUrl"])

                        #Additional ingredients
                        missing_ingredients = []
                        if recipes[i]["missedIngredientCount"] > 0:
                            for j in range(len(recipes[i]["missedIngredients"])):
                                missing_ingredients.append(recipes[i]["missedIngredients"][j]["name"])
                        st.write(f"You will need the following additional ingredients: {missing_ingredients}")

            else:
                st.write("Sorry, we couldn't find any recipes")
    else:
        st.write("We couldn't find any ingredients on the picture, please upload another file")

background()
