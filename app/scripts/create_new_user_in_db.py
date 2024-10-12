import base64
import os
import requests

from dotenv import load_dotenv, find_dotenv


async def create_new_user_in_db(name: str, phone: str, medical_organization: str) -> int | None:
    load_dotenv(find_dotenv())

    url = 'https://helpdesk.across.ru/api/v2/users/'

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "email": f'{phone}@auto.bot',
        "phone": phone,
        "organization": medical_organization,
        "department": [1, 2],
        "group_id": 1,
        "password": 123
    }

    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        return response.json()['data']['id']

    return None