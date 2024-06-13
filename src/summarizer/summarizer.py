import json
import time

import requests


class Summarizer:
    def __init__(self, catalogue: str, api_key: str) -> None:
        self.catalogue = catalogue
        self.api_key = api_key

    def summarize(self, article: str) -> str:
        api_url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

        data = {
            "modelUri": f"gpt://{self.catalogue}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0,
                "maxTokens": "2000"
            },
            "messages": [
                {
                "role": "system",
                "text": "Сократи текст до 30-50 слов. Не возвращай текст связанный"
                },
                {
                "role": "user",
                "text": article
                }
            ]
        }

        jsondata = json.dumps(data)
        headers = {
            'Authorization': f'Api-Key {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(api_url, headers=headers, data=jsondata)
        time.sleep(2)
        if response.status_code == 200:
            print('Successfully summarized')
            result = response.json()['result']['alternatives'][0]['message']['text']
            if 'я не могу ничего сказать об этом' in result.lower() or 'давайте сменим тему' in result.lower():
                return article[:200] + '...'
            return result
        else:
            print(f'[ERROR] :: {response.status_code, response.text}')
            return article[:200] + '...'
