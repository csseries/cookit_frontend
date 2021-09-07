import streamlit as st
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions
from cookit_frontend.image import resize_image, pil_to_buffer
from cookit_frontend.page_elements import *
from cookit_frontend.utils import INGREDIENTS, LEVELS
from cookit_frontend.query import find_recipes_in_db, open_db_connection


page_decorators()
local_css("style.css")

page_header()

uploaded_file = page_pic_uploader()

# establish db connection and keep it open in the cache
db_conn = open_db_connection()

if uploaded_file:
    resized_file = resize_image(uploaded_file)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write("")
    with col2:
        gif_runner = st.image("frontend_img/giphy.gif")
        ingredients, scores, bboxes = get_predictions(pil_to_buffer(resized_file))
        gif_runner.empty()
    with col3:
        st.write("")

    if len(ingredients) > 0:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("")
            show_bbox_image(resized_file, bboxes, ingredients, scores)
            st.write("")

        with col2:
            # do not add nonsense ingredients to the list (like "Fruit")
            filtered_ingredients = [ingr for ingr in ingredients if ingr in INGREDIENTS]
            ingredients_selected = st.multiselect("We found these ingredients (delete any you don't want to use)",
                                                  filtered_ingredients, default=filtered_ingredients)

            must_haves = st.multiselect('You can add more ingredients', INGREDIENTS)

            exclusions = st.multiselect("Anything you really don't like?", INGREDIENTS)

            #Specify level of recipe difficulty
            #difficulty = st.selectbox("How difficult should your recipe be?", LEVELS)

        if st.button('get recipes'):
            recipes = find_recipes_in_db(db_conn, ingredients_selected + must_haves, exclusions)

            if len(recipes) > 0:
                show_recipes(recipes, 3)
            else:
                st.warning("Sorry, we couldn't find any recipes")
    else:
        st.warning("We can't identify the ingredients in the picture, please upload another one")
