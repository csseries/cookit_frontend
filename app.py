import streamlit as st
import os
import base64
from PIL import Image
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions
from cookit_frontend.image import resize_image, draw_boxes, pil_to_buffer
from cookit_frontend.page_elements import *
from load_css import local_css

page_decorators()

local_css("style.css")

page_title()

#page_slogan()

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

    # All veg and fruit classes plus cheese and egg from Open Images Dataset V6
    food_classes_oiv6 = ['Apple', 'Artichoke', 'Banana', 'Beer', 'Bell pepper',\
                   'Bread', 'Broccoli', 'Cabbage', 'Cantaloupe', 'Carrot',\
                   'Cheese', 'Coconut', 'Cucumber', 'Egg',\
                   'Garden Asparagus', 'Grape', 'Grapefruit', 'Lemon',\
                   'Mango', 'Mushroom', 'Orange', 'Pear', 'Pineapple',\
                   'Pomegranate', 'Potato', 'Pumpkin', 'Radish', 'Squash',\
                   'Strawberry', 'Tomato', 'Watermelon', 'Zucchini']

    if len(ingredients) > 0:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("")
            show_bbox_image(resized_file, bboxes, ingredients, scores)
            st.write("")

        with col2:
            ingredients_selected = st.multiselect("We found these ingredients (delete any you don't want to use)", ingredients, default=ingredients)
            ingredients_selected_formatted = ", ".join(ingredients_selected)

            must_haves = st.multiselect('You can add more ingredients', food_classes_oiv6)
            must_haves_formatted = ", ".join(must_haves)

            exclusions = st.multiselect("Anything you really don't like?", food_classes_oiv6)
            exclusions_formatted = ", ".join(exclusions)

            #A comma-separated list of cuisines
            cuisine = st.multiselect('Which cuisine do you feel like today?', all_cuisines)
            cuisines_formatted = ", ".join(cuisine)

            #Specify a specific diet
            diet = st.selectbox("Do you have any dietary restrictions?", dietary_resitrictions)
            if diet == "I eat everything":
                diet = []

        if st.button('get recipes'):
            recipes = get_recipes(ingredients_selected_formatted, must_haves_formatted, exclusions, cuisines_formatted, diet)

            if len(recipes) > 0:
                show_recipes(recipes, 3)
            else:
                st.write("Sorry, we couldn't find any recipes")
    else:
        st.write("We couldn't find any ingredients on the picture, please upload another file")

background()
