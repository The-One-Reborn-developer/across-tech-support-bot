import base64, os, requests

from dotenv import load_dotenv, find_dotenv


async def send_request(name: str, position: str, region: str, phone: str, medical_organization: str) -> int | None:
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
        "password": 
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
    print(response.json())