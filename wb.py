import requests
import time
import json
import gpt_generator
import config
import bot
import utils
import mock_db


BASE_URL = 'https://feedbacks-api.wildberries.ru/'
FEEDBACK_TIMEOUT = 120
LOCAL_TIMEOUT = 10


def get_feedbacks(auth):
    url = 'api/v1/feedbacks'
    headers = {'Authorization': auth}
    params ={'isAnswered': False,
             'take': 100, 
             'skip': 0}
    response = requests.get(BASE_URL + url, headers=headers, params=params)
    return response


if __name__ == '__main__':
    bot.send_text_message('Начали')
    i = 0
    while True:
        i += 1
        if i % 2:
            auth = config.WB_TOKEN_OOO
        else:
            auth = config.WB_TOKEN_IP
        response = get_feedbacks(auth)
        for feedback in response.json()['data']['feedbacks']:
            if feedback['id'] in mock_db.db:
                continue
                
            parsed_feedback = utils.parse_feedback(feedback)
            bot.send_text_message(json.dumps(parsed_feedback, ensure_ascii=False))
            reply = gpt_generator.get_reply(parsed_feedback)
            bot.send_text_message(reply)
            mock_db.db.append(feedback['id'])

            time.sleep(LOCAL_TIMEOUT)
        time.sleep(FEEDBACK_TIMEOUT)

