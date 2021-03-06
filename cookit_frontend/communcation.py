import os
import requests
import streamlit as st

if 'LOCAL_BACKEND_URL' in os.environ:
    BACKEND_URL = os.environ['LOCAL_BACKEND_URL']
    print('Send requests to local cookit backend url: ', BACKEND_URL)
else:
    BACKEND_URL = 'https://fast-drake-318911-6gdu3ouwsa-ey.a.run.app/predict'
    print('Send requests to remote backend url: ', BACKEND_URL)


@st.cache(show_spinner=False)
def get_predictions(image):
    files = {'image': image}
    payload = {'threshold': 0.3}
    response = requests.post(BACKEND_URL, files=files, data=payload)

    if response.status_code == 200:
        res = response.json()
        print('Received predictions: ', res)
        return (res['prediction'], res['scores'], res['bboxes'])

    print(f'Something went wong. Received code {response.status_code}')
    return ([], [], [])
