import time
import httpx
from config import PROXY, GPT_KEY, WB_TOKEN_OOO


PROXY_CHECK_URL = 'https://api.ipify.org?format=json'
GPT_CHECK_URL = 'https://api.openai.com/v1/models'
WB_CHECK_URL = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'


def check_proxy(proxy: str, timeout_s: float = 10.0):
    try:
        with httpx.Client(proxy=proxy, timeout=timeout_s) as client:
            t0 = time.perf_counter()
            r = client.get(PROXY_CHECK_URL)
            r.raise_for_status()
            ip = r.json().get("ip")
            return ip, str(int((time.perf_counter() - t0) * 1000)) + 'ms'
    except Exception:
        return None
    


def check_openai(proxy: str, api_key: str, timeout_s: float = 15.0):
    """
    403 - without proxy
    401 - gpt token problem
    None - запрос не дошел
    """
    try:
        with httpx.Client(
            proxy=proxy,
            timeout=timeout_s,
            headers={"Authorization": f"Bearer {api_key}"},
        ) as c:
            r = c.get(GPT_CHECK_URL)
        return (200 <= r.status_code < 300), r.status_code

    except httpx.HTTPStatusError as e:
        # если где-то выше будет raise_for_status(), но здесь не обязателен
        return False, e.response.status_code

    except httpx.HTTPError as e:
        resp = getattr(e, "response", None)
        return False, (resp.status_code if resp is not None else None)

    except Exception:
        return False, None
    

def check_wb(wb_token, timeout_s: float = 10.0):
    headers = {'Authorization': wb_token}
    params ={'isAnswered': False,
             'take': 100, 
             'skip': 0}
    try:
        with httpx.Client(timeout=timeout_s) as c:
            r = c.get(WB_CHECK_URL, headers=headers, params=params)
        return r.is_success, r.status_code
    except httpx.HTTPError as e:
        return False, getattr(getattr(e, "response", None), "status_code", None)

    
if __name__ == '__main__':
    print(check_wb(WB_TOKEN_OOO + 'f'))