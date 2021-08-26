import streamlit as st
import os
import base64
from PIL import Image
from cookit_frontend.recipes import get_recipes
from cookit_frontend.communcation import get_predictions

st.set_page_config(page_title='cookit', page_icon="frontend_img/favicon.png")

'''
# Cookit
'''
#Logo + slogan
#img = Image.open("frontend_img/logo.png")
#st.image(img)

#To Do: Add Logo

st.write('Upload pictures of your ingredients and get recipe suggestions based on what you have at home!')

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


#Creating background

@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

image_path = 'frontend_img/background.png'

st.write(background_image_style(image_path), unsafe_allow_html=True)
