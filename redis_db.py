import redis
import json


redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
key = "wb_feedbacks"
automod_key = 'wb_automod_rates'

def add_redis(item: dict):
    redis_client.rpush(key, json.dumps(item, ensure_ascii=False))

def get_all_redis():
    raw_items = redis_client.lrange(key, 0, -1)         
    items = [json.loads(x) for x in raw_items]
    return items

def clear_list():
    redis_client.delete(key)

def get_selected_rates() -> list[int]:
    raw = redis_client.get(automod_key)
    if not raw:
        return []
    try:
        arr = json.loads(raw)
        return [int(x) for x in arr] if isinstance(arr, list) else []
    except Exception:
        return []

def set_selected_rates(arr: list[int]) -> None:
    redis_client.set(automod_key, json.dumps([int(x) for x in arr]))

