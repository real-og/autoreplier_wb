import os
import httpx
from openai import OpenAI
import config
import json
from openai import OpenAI



http_client = httpx.Client(
    proxy=config.PROXY,          # актуальный параметр в новых httpx
    timeout=60.0,
)

client = OpenAI(api_key=config.GPT_KEY, http_client=http_client)

INSTRUCTIONS = (
    "Ты — служба поддержки продавца на Wildberries. "
    "Сгенерируй ВЕЖЛИВЫЙ, КОРОТКИЙ ответ продавца на отзыв покупателя на русском. "
    "Правила: 1-3 предложения, без ссылок, без обещаний того, чего не знаешь, без 'мы лучшие'. "
    "Если отзыв пустой и 5★ — просто поблагодари и пожелай приятного пользования. "
    "Если есть 'cons' или низкая оценка — извинись, уточни проблему, предложи написать в поддержку/вопросы в WB."
)

SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"}
    },
    "required": ["answer"],
    "additionalProperties": False
}

def get_reply(payload: dict) -> str:

    resp = client.responses.create(
        model="gpt-5-mini",
        instructions=INSTRUCTIONS,
        input="Данные отзыва (JSON):\n" + json.dumps(payload, ensure_ascii=False),
        max_output_tokens=1000,
        text={
            "format": {
                "type": "json_schema",
                "name": "wb_reply",
                "strict": True,
                "schema": SCHEMA
            }
        },
        store=False,  
    )

    raw = resp.output_text

    print("status:", getattr(resp, "status", None))
    print("error:", getattr(resp, "error", None))
    print("incomplete_details:", getattr(resp, "incomplete_details", None))
    print("output_len:", len(getattr(resp, "output", []) or []))
    print("raw repr:", repr(raw))
    if not raw or not raw.strip():
        print(resp.model_dump_json(indent=2, ensure_ascii=False))
        raise RuntimeError("Empty output_text (no output_text blocks in response)")
    
    data = json.loads(resp.output_text)
    return data["answer"].strip()



if __name__ == '__main__':
    print(get_reply('класс'))
    
