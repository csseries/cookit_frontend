import requests

BACKEND_URL = 'https://fast-drake-318911-6gdu3ouwsa-ey.a.run.app/predict'


def get_predictions(image):
    #files = {'image': open(image, 'rb')}
    files = {'image': image}
    response = requests.post(BACKEND_URL, files=files)
    print(response)
    if response.status_code == 200:
        return response.json()['prediction']

    return []
