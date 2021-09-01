import streamlit as st
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions
from cookit_frontend.image import resize_image, pil_to_buffer
from cookit_frontend.page_elements import *
from cookit_frontend.utils import INGREDIENTS, DIETARY_RESTRICTIONS, CUISINES

page_decorators()
local_css("style.css")

page_header()

uploaded_file = page_pic_uploader()

#Option to upload jpg/ png image that will be used from the model


if uploaded_file:
    resized_file = resize_image(uploaded_file)
    ingredients, scores, bboxes = get_predictions(pil_to_buffer(resized_file))

    if len(ingredients) > 0:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("")
            show_bbox_image(resized_file, bboxes, ingredients, scores)
            st.write("")

        with col2:
            ingredients_selected = st.multiselect("We found these ingredients (delete any you don't want to use)", ingredients, default=ingredients)
            ingredients_selected_formatted = ", ".join(ingredients_selected)

            must_haves = st.multiselect('You can add more ingredients', INGREDIENTS)
            must_haves_formatted = ", ".join(must_haves)

            exclusions = st.multiselect("Anything you really don't like?", INGREDIENTS)
            exclusions_formatted = ", ".join(exclusions)

            #A comma-separated list of cuisines
            cuisine = st.multiselect('Which cuisine do you feel like today?', CUISINES)
            if cuisine == "I don't have any preferences":
                cuisine = []

            cuisines_formatted = ", ".join(cuisine)


            #Specify a specific diet
            diet = st.selectbox("Do you have any dietary restrictions?", DIETARY_RESTRICTIONS)
            if diet == "I eat everything":
                diet = []

        if st.button('get recipes'):
            recipes = get_recipes(ingredients_selected_formatted, must_haves_formatted, exclusions, cuisines_formatted, diet)

            if len(recipes) > 0:
                show_recipes(recipes, 3)
            else:
                st.write("<span class='body'>Sorry, we couldn't find any recipes</span>", unsafe_allow_html=True)
    else:
        st.write("<span class='body'>We can't identify the ingredients in the picture, please upload another one</span>", unsafe_allow_html=True)

background()
