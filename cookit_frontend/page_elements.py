import streamlit as st
import os
import base64
from PIL import Image


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