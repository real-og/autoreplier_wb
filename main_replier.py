import requests
import time
import json
import gpt_generator
import config
import sender
import utils
import keyboards as kb
import wb_api
import redis_db



FEEDBACK_TIMEOUT = 1
LOCAL_TIMEOUT = 1





if __name__ == '__main__':
    sender.send_text_message('Начали')
    i = 0
    while True:
        i += 1
        if i % 2:
            auth = config.WB_TOKEN_OOO
        else:
            auth = config.WB_TOKEN_IP
        response_feedbacks = wb_api.get_feedbacks(auth)

        for feedback in response_feedbacks.json()['data']['feedbacks']:
            answered = redis_db.get_all_redis()
            to_skip = False
            for item in answered:
                if feedback['id'] == item['feedback_id']:
                    to_skip = True
            if to_skip:
                continue
                
            parsed_feedback = utils.parse_feedback(feedback)

            message_id = sender.send_text_message(json.dumps(parsed_feedback, ensure_ascii=False))
            if auth == config.WB_TOKEN_OOO:
                account = 'OOO'
            elif auth == config.WB_TOKEN_IP:
                account = 'IP'

            reply_gpt = gpt_generator.get_reply(parsed_feedback)
            reply_id = sender.send_text_message(reply_gpt, kb.to_send_kb)

            redis_db.add_redis({'timestamp': int(time.time()),
                               'feedback_id': feedback['id'],
                               'account': account,
                               'message_id': message_id,
                               'reply_message_id': reply_id})
            

            time.sleep(LOCAL_TIMEOUT)
        time.sleep(FEEDBACK_TIMEOUT)

