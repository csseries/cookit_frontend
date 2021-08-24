import streamlit as st
from cookit_frontend.recipes import get_recipes



'''
# Cookit
'''

#To Do: Add Logo

st.write('Upload a picture from your fridge or pantry and get recipe suggestions')
#Option to upload jpg/ png image that will be used from the model

#For now we use a list of ingredients, later we need a list from the model that will be used for the API call
ingredients = st.text_input('Add some ingredients (comma-separated)', 'Garlic, Butter, Cucumber')
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
