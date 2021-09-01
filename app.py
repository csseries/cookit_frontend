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
            ingredients_selected = st.multiselect("We found these ingredients (delete any you don't want to use)",
                                                  ingredients, default=ingredients)
            ingredients_selected_formatted = ", ".join(ingredients_selected)

            must_haves = st.multiselect('You can add more ingredients', INGREDIENTS)
            must_haves_formatted = ", ".join(must_haves)

            exclusions = st.multiselect("Anything you really don't like?", INGREDIENTS)
            exclusions_formatted = ", ".join(exclusions)

            #A comma-separated list of cuisines
            cuisine = st.multiselect('Which cuisine do you feel like today?',
                                     CUISINES, default=CUISINES[0])
            if cuisine == CUISINES[0]:
                cuisine = []

            cuisines_formatted = ", ".join(cuisine)


            #Specify a specific diet
            diet = st.selectbox("Do you have any dietary restrictions?", DIETARY_RESTRICTIONS)
            if diet == "I eat everything":
                diet = []

        if st.button('get recipes'):
            recipes = get_recipes(f"{ingredients_selected_formatted}, {must_haves_formatted}",
                                  exclusions, cuisines_formatted, diet)

            if len(recipes) > 0:
                show_recipes(recipes, 3)
            else:
                st.warning("Sorry, we couldn't find any recipes")
    else:
        st.warning("We can't identify the ingredients in the picture, please upload another one")
