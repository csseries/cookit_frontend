import streamlit as st
from cookit_frontend.recipes import get_recipes



'''
# cookit
'''

st.write('Not much to see here yet')

ingredients = st.text_input('Add some ingredients (comma-separated)', 'Garlic, Butter, Cucumber')
ingredients_parsed = [ingr for ingr in ingredients.split(',')]

# this is just to avoid making too many requests during development
if st.button('get recipes'):
    recipes = get_recipes(ingredients_parsed)
    for recipe in recipes:
        st.image(recipe['image'], caption=recipe['title'], use_column_width=False)
