import streamlit as st
import os
import base64
from PIL import Image
from cookit_frontend.image import draw_boxes



def local_css(file_name):
    '''loads the local 'style.css' file into the app'''
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def page_decorators():
    return st.set_page_config(page_title='cookit', page_icon="frontend_img/favicon.png", layout="wide")


def page_title():
    img = Image.open("frontend_img/logo_crop.png")
    # create a padding on top
    # row_top_1, row_top_2 = st.columns([1, 1])
    # with row_top_1:
    #     #st.write("")
    #     st.image(img)
    # with row_top_2:
    #     st.write("")

    #
    col1, col2 = st.columns([2, 2])
    with col1:
        st.image(img)
        st.write("")
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        page_slogan()
    #return col1, col2


def page_slogan():
    write_text("<span class='body'>Use what's in your fridge (or pantry): \
    <br> \
    <br>1️⃣ Take a picture <br>2️⃣ Upload it <br>3️⃣ Receive recipe suggestions</span>")


def page_pic_uploader():
    col1, col2, col3 = st.columns([1, 2, 1])
    # with col1:
    #     st.file_uploader("Upload picture(s)", type=["png", "jpg"], accept_multiple_files=False)
    # with col2:
    #     st.write("")
    #return col1, col2
    write_text("<span class='body'>Upload picture(s)</span>")
    return st.file_uploader("", type=["png", "jpg", "jpeg"], accept_multiple_files=False)


def show_bbox_image(resized_file, bboxes, ingredients, scores):
    bbox_image = draw_boxes(resized_file, bboxes, ingredients, scores)
    st.image(bbox_image)

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

    #TODO refactor. currently
    # Adjust column layout to number of recipes. Ideally there are three
    # columns of recipes. If there is only one, put it in the middle, if two,
    # in columns 1 and 2
    col1, col2, col3 = st.columns([2, 2, 2])
    if len(recipes) == 1 or display_count == 1:
        with col1:
            st.write("")
        with col2:
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[0]['image'], recipes[0]["sourceUrl"])
            st.markdown(f"### {recipes[0]['title']}")
            st.write(f"Time: {recipes[0]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[0]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[0]["missedIngredientCount"] > 0:
                for ingr in recipes[0]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)

    elif len(recipes) == 2 or display_count == 2:
        with col1:
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[0]['image'], recipes[0]["sourceUrl"])
            st.markdown(f"### {recipes[0]['title']}")
            st.write(f"Time: {recipes[0]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[0]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[0]["missedIngredientCount"] > 0:
                for ingr in recipes[0]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)
        with col2:
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[1]['image'], recipes[1]["sourceUrl"])
            st.markdown(f"### {recipes[1]['title']}")
            st.write(f"Time: {recipes[1]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[1]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[1]["missedIngredientCount"] > 0:
                for ingr in recipes[1]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)

    else:
        with col1:
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[0]['image'], recipes[0]["sourceUrl"])
            st.markdown(f"### {recipes[0]['title']}")
            st.write(f"Time: {recipes[0]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[0]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[0]["missedIngredientCount"] > 0:
                for ingr in recipes[0]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)
        with col2:
            st.write(" ") # makes sure we are vertically aligned with col2
            show_img_with_href(recipes[1]['image'], recipes[1]["sourceUrl"])
            st.markdown(f"### {recipes[1]['title']}")
            st.write(f"Time: {recipes[1]['readyInMinutes']} minutes")
            st.write("[Cookit !] (%s)" % recipes[1]["sourceUrl"])

            #Additional ingredients
            missing_ingredients = []
            if recipes[1]["missedIngredientCount"] > 0:
                for ingr in recipes[1]["missedIngredients"]:
                    missing_ingredients.append(ingr["name"].capitalize())
            st.markdown(f"""
                        You'll need these additional ingredients:

                        {", ".join(missing_ingredients)}
                        """)

            with col3:
                st.write(" ") # makes sure we are vertically aligned with col2
                show_img_with_href(recipes[2]['image'], recipes[2]["sourceUrl"])

                st.markdown(f"### {recipes[2]['title']}")
                st.write(f"Time: {recipes[2]['readyInMinutes']} minutes")
                st.write("[Cookit !] (%s)" % recipes[2]["sourceUrl"])

                #Additional ingredients
                missing_ingredients = []
                if recipes[2]["missedIngredientCount"] > 0:
                    for ingr in recipes[2]["missedIngredients"]:
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
