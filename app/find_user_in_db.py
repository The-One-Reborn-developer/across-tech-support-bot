import base64
import os
import requests

from dotenv import load_dotenv, find_dotenv


async def find_user_in_db(phone: str) -> int | None:
    load_dotenv(find_dotenv())

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}",
        "Content-Type": "application/json"
    }

    initial_url = f'https://helpdesk.across.ru/api/v2/users/?page=1'

    response = requests.get(initial_url, headers=headers)
    response_json = response.json()
    
    total_pages = response_json['pagination']['total_pages']

    for page in range(1, total_pages + 1):
        url = f'https://helpdesk.across.ru/api/v2/users/?page={page}'

        response = requests.get(url, headers=headers)
        response_json = response.json()

        for user in response_json['data']:
            if user['phone'] == phone:
                return user['id']

    return None