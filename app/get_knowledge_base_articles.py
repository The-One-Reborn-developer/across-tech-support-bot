import base64
import os
import requests

from dotenv import load_dotenv, find_dotenv


async def get_knowledge_base_articles() -> dict:
    load_dotenv(find_dotenv())

    url = 'https://helpdesk.across.ru/api/v2/knowledge_base/articles/?category_list=3'

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    return response.json()