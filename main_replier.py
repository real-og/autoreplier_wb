import requests
import time
import json
import gpt_generator
import config
import bot_outer_interface
import utils
import keyboards as kb
import wb_api
import redis_db
import traceback
from datetime import datetime
import texts



FEEDBACK_TIMEOUT = 5
LOCAL_TIMEOUT = 3
EXCEPTION_TIMEOUT = 120



if __name__ == '__main__':
    bot_outer_interface.send_text_message('Начали')
    i = 0
    while True:
        try:

            # circling 2 shops via 2 tokens
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
                message_to_send = utils.compose_message(feedback)

                message_id = bot_outer_interface.send_text_message(message_to_send)
                if auth == config.WB_TOKEN_OOO:
                    account = 'OOO'
                elif auth == config.WB_TOKEN_IP:
                    account = 'IP'

                reply_gpt = gpt_generator.get_reply(parsed_feedback)
                reply_id = bot_outer_interface.send_text_message(reply_gpt, kb.to_send_kb)

                redis_db.add_redis({'timestamp': int(time.time()),
                                'feedback_id': feedback['id'],
                                'account': account,
                                'message_id': message_id,
                                'reply_message_id': reply_id})
                
                rates_to_auto_reply = redis_db.get_selected_rates()
                if (parsed_feedback['rating'] is not None) and int(parsed_feedback['rating']) in rates_to_auto_reply:
                    wb_api.answer_feedback_mock(auth, feedback['id'], reply_gpt)
                    bot_outer_interface.edit_kb(reply_id, kb.done_auto_kb)
                

                time.sleep(LOCAL_TIMEOUT)
            time.sleep(FEEDBACK_TIMEOUT)
        except Exception as e:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('EXCEPTION MAIN_REPLIER')
            print(ts)
            print(traceback.format_exc())
            bot_outer_interface.send_text_message(texts.error_alert)
            time.sleep(EXCEPTION_TIMEOUT)
        


