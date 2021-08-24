import streamlit as st
import os
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions



'''
# Cookit
'''

#To Do: Add Logo

st.write('Simply upload a picture of your ingredients and get recipe suggestions based on what you have at home!')

#Option to upload jpg/ png image that will be used from the model
uploaded_file = st.file_uploader("Upload picture(s) of your fridge or pantry", type=["png", "jpg"], accept_multiple_files=False)

if uploaded_file:
    ingredients = get_predictions(uploaded_file)

    if len(ingredients) > 0:
        #For now we use a list of ingredients, later we need a list from the model that will be used for the API call
        ingredients = st.text_input('Manually adjust ingredients (comma-separated)', ', '.join(ingredients))
        ingredients_parsed = [ingr for ingr in ingredients.split(',')]

        must_haves = st.text_input('Add ingredients that must be included (comma-separated)', 'Tomato')
        must_haves_parsed = [must for must in must_haves.split(',')]

        exclusions = st.text_input("What don't you like in your food? (comma-separated)", "Coriander, Basil")
        exclusions_parsed = [excl for excl in exclusions.split(',')]

        #Add cuisine preferences with checkboxes

        # this is just to avoid making too many requests during development
        if st.button('get recipes'):
            recipes = get_recipes(ingredients_parsed, must_haves_parsed, exclusions_parsed)

            if len(recipes) > 0:
                for i in range(min(len(recipes), 10)):
                    st.image(recipes[i]['image'], recipes[i]['title'], use_column_width=False)
                    url = recipes[i]["sourceUrl"]
                    st.write("Cook this [recipe](%s) now" % url)
            elif len(recipes) == 0:
                st.write("Sorry, we couldn't find any recipes")
