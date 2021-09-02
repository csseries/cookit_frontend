import streamlit as st
import os
import base64
from PIL import Image
from cookit_frontend.image import draw_boxes



def local_css(file_name):
    '''loads the local 'style.css' file into the app'''
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def page_decorators():
    st.set_page_config(page_title='cookit', page_icon="frontend_img/favicon.png")


def page_header():
    img = Image.open("frontend_img/logo_crop.png")
    background()

    #st.image(img)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.write("")
    with col2:
        st.image(img)
        page_slogan()
    with col3:
        st.write("")


def page_slogan():
    write_text("<span class='slogan'> \
                    <p>Use what's in your fridge (or pantry)</p> \
                    <br> \
                    <br>1️⃣ Take a picture \
                    <br>2️⃣ Upload it \
                    <br>3️⃣ Receive recipe suggestions \
                </span>")


def page_pic_uploader():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.write("")
    with col2:
        uploaded_file = st.file_uploader("Upload picture(s)", type=["png", "jpg", "jpeg"], accept_multiple_files=False)
    with col3:
        st.write("")
    return uploaded_file

def show_bbox_image(resized_file, bboxes, ingredients, scores):
    bbox_image = draw_boxes(resized_file, bboxes, ingredients, scores)
    st.image(bbox_image)

def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded



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


def show_recipes(recipes, display_count=3):
    recipes_to_show = min(len(recipes), display_count)
    display_cols = [1 for count in range(recipes_to_show)]
    cols = st.columns(display_cols)
    for i in range(recipes_to_show):
        with cols[i]:
            show_img_with_href(recipes[i]['image'], recipes[i]["sourceUrl"])
            st.markdown(f"### {recipes[i]['title']}")
            st.write(f"Time: {recipes[i]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[i]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[i]["missedIngredientCount"] > 0:
                for ingr in recipes[i]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

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
