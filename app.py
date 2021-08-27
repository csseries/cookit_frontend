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

    food_preferences = ['Italian', 'German', 'French', 'Vegetarian']

    if len(ingredients) > 0:
        bbox_image = draw_boxes(resized_file, bboxes, ingredients, scores)
        st.image(bbox_image)

        ingredients_selected = st.multiselect('Check ingredients to include in recipes', ingredients, default=ingredients)
        must_haves = st.multiselect('Add ingredients that must be included', ingredients_selected)
        exclusions = st.text_input("What don't you like in your food? (comma-separated)")
        exclusions_parsed = [excl for excl in exclusions.split(',')]
        ingredients_selected = st.multiselect('What type of food do you prefer?', food_preferences, default=food_preferences) 
        # to be refined and link to recipe search

        # this is just to avoid making too many requests during development
        if st.button('get recipes'):
            recipes = get_recipes(ingredients_selected, must_haves, exclusions_parsed)

            if len(recipes) > 0:
                for i in range(min(len(recipes), 10)):
                    col1, col2 = st.columns([3,5])
                    with col1:
                        st.image(recipes[i]['image'], use_column_width=True)
                    with col2:
                        st.write(recipes[i]['title'])
                        st.write("Cook this [recipe](%s) now" % recipes[i]["sourceUrl"])
                    
            elif len(recipes) == 0:
                st.write("Sorry, we couldn't find any recipes")
    else:
        st.write("We couldn't find any ingredients on the picture, please upload another file")

background()
