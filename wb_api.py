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


def get_feedback_by_id(auth, id):
    url = 'api/v1/feedback'
    headers = {'Authorization': auth}
    params ={'id': id}
    response = requests.get(BASE_URL + url, headers=headers, params=params)
    return response


# auth - wb token; id - feedback-id from wb
def answer_feedback(auth, id: str, text: str):
    url = 'api/v1/feedbacks/answer'
    headers = {'Authorization': auth,
               'Content-Type': 'application/json'}
    body ={'id': id,
           'text': text}
    response = requests.post(BASE_URL + url, headers=headers, json=body)
    return response.status_code


def answer_feedback_mock(auth, id: str, text: str):
    print('mock answer')
    print(auth)
    print(id)
    print(text)
    return 204