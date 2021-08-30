import streamlit as st
import os
import base64
from PIL import Image

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def page_decorators():
    return st.set_page_config(page_title='cookit', page_icon="frontend_img/favicon.png")


def page_title():
    img = Image.open("frontend_img/logo.png")
    col1, col2, col3 = st.columns([3,3,3])
    with col1:
        st.write("")
    with col2:
        st.image(img)
    with col3:
        st.write("")
    return col1, col2, col3


def page_slogan():
    return write_text('Upload pictures of your ingredients and get recipe suggestions based on what you have at home!')

def page_pic_uploader():
    return st.file_uploader("Upload picture(s) of your fridge or pantry", type=["png", "jpg"], accept_multiple_files=False)


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


def write_text(text):
    return st.write(text, unsafe_allow_html=True)


def background():
    image_path = 'frontend_img/background.png'
    return st.write(background_image_style(image_path), unsafe_allow_html=True)


def show_recipes(recipes, display_count):
    print(f"Display {display_count} out of {len(recipes)} recipes")
    for i in range(min(len(recipes), display_count)):
        col1, col2 = st.columns([4, 5])
        with col1:
            #st.image(recipes[i]['image'], use_column_width=True)
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[i]['image'], recipes[i]["sourceUrl"])
        with col2:
            st.markdown(f"### {recipes[i]['title']}")
            st.write(f"Cooking time: {recipes[i]['readyInMinutes']} minutes")
            st.write("Cook this [recipe](%s) now" % recipes[i]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[i]["missedIngredientCount"] > 0:
                for ingr in recipes[i]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You will need the following additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)

#@st.cache(allow_output_mutation=True)
def show_img_with_href(img_url, target_url):
    """ Display image with href in new browser tab"""
    html_code = f'''
        <a href="{target_url}" target="_blank" rel="noopener noreferrer">
            <img src="{img_url}" style="width: 90%"/>
        </a>'''
    st.markdown(html_code, unsafe_allow_html=True)
