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

    if len(ingredients) > 0:
        bbox_image = draw_boxes(resized_file, bboxes, ingredients, scores)
        st.image(bbox_image)

        ingredients_selected = st.multiselect('Check ingredients to include in recipes', ingredients, default=ingredients)
        must_haves = st.multiselect('Add ingredients that must be included', ingredients_selected)
        exclusions = st.text_input("What don't you like in your food? (comma-separated)")
        exclusions_parsed = [excl for excl in exclusions.split(',')]

        #Add cuisine preferences with checkboxes

        # this is just to avoid making too many requests during development
        if st.button('get recipes'):
            recipes = get_recipes(ingredients_selected, must_haves, exclusions_parsed)

            if len(recipes) > 0:
                for i in range(min(len(recipes), 10)):
                    st.image(recipes[i]['image'], recipes[i]['title'], use_column_width=False)
                    url = recipes[i]["sourceUrl"]
                    st.write("Cook this [recipe](%s) now" % url)
            elif len(recipes) == 0:
                st.write("Sorry, we couldn't find any recipes")
    else:
        st.write("We couldn't find any ingredients on the picture, please upload another file")

background()
