import requests
import streamlit as st

#BACKEND_URL = 'https://fast-drake-318911-6gdu3ouwsa-ey.a.run.app/predict'
BACKEND_URL = 'http://localhost:8000/predict'

@st.cache(suppress_st_warning=True)
def get_predictions(image):
    files = {'image': image}
    response = requests.post(BACKEND_URL, files=files)

    if response.status_code == 200:
        res = response.json()
        print('Received predictions: ', res['prediction'])
        return (res['prediction'], res['scores'], res['bboxes'])
    print(f'Something went wong. Received code {response.status_code}')
    return []
