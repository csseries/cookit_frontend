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

exclusions = st.text_input("What don't you like in your food? (comma-separated)", "Coriander, Basil")
exclusions_parsed = [excl for excl in exclusions.split(',')]

#Add cuisine preferences with checkboxes

# this is just to avoid making too many requests during development
if st.button('get recipes'):
    recipes = get_recipes(ingredients_parsed, exclusions_parsed)

    if len(recipes) > 0:
        for i in range(min(len(recipes), 10)):
            st.image(recipes[i]['image'], recipes[i]['title'], use_column_width=False)

        #Add link to the orginal recipe next to the picture or underneath
        #recipes[i]["sourceUrl"]

    elif len(recipes) == 0:
        st.write("Sorry, we couldn't find any recipes")
