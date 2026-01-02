# redis_client.py
import redis
import json

redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
key = "wb_feedbacks"

def add_redis(item: dict):
    redis_client.rpush(key, json.dumps(item, ensure_ascii=False))

def get_all_redis():
    raw_items = redis_client.lrange(key, 0, -1)         
    items = [json.loads(x) for x in raw_items]
    return items

def clear_list():
    redis_client.delete(key)
