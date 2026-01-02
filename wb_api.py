import requests

BASE_URL = 'https://feedbacks-api.wildberries.ru/'


def get_feedbacks(auth):
    url = 'api/v1/feedbacks'
    headers = {'Authorization': auth}
    params ={'isAnswered': False,
             'take': 100, 
             'skip': 0}
    response = requests.get(BASE_URL + url, headers=headers, params=params)
    return response


def answer_feedback___(auth, id: str, text: str):
    url = 'api/v1/feedbacks/answer'
    headers = {'Authorization': auth,
               'Content-Type': 'application/json'}
    body ={'id': id,
           'text': text}
    response = requests.post(BASE_URL + url, headers=headers, json=body)
    return response.status_code


def answer_feedback_mock(auth, id: str, text: str):
    print(auth)
    print(id)
    print(text)
    return 204