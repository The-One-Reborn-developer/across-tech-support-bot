import base64, os, requests

from dotenv import load_dotenv, find_dotenv

from app.database.requests import set_ticket


async def create_ticket(
        telegram_id: int,
        user_id: int,
        chat_id: int,
        user_region: str,
        user_position: str,
        request_type: str,
        request_description: str,
        has_photo: bool) -> int | None:
    load_dotenv(find_dotenv())

    url = 'https://helpdesk.across.ru/api/v2/tickets'

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}"
    }

    if request_type == "critical":
        request_type_data = "Критическая ошибка ЛИС"
    elif request_type == "no_exchange":
        request_type_data = "Нет обмена с МИС"
    elif request_type == "no_connection":
        request_type_data = "Нет связи с анализаторами"
    elif request_type == "other":
        request_type_data = "Другое"

    description_data = f"{request_description}; " + \
                        f"Регион: {user_region}; " + \
                        f"Должность: {user_position}"

    if has_photo:
        file_path = f"app/photos/{telegram_id}.jpg"
        
        payload = {
            "title": request_type_data,
            "description": description_data,
            "user_id": user_id,
            "custom_fields[12]": '16'
        }
        
        files = [
            ('files[]',
            (f"{telegram_id}.jpg",
            open(file_path, 'rb'),
            'image/jpeg'))
        ]

        response = requests.post(url, headers=headers, data=payload, files=files)
    else:
        payload = {
            "title": request_type_data,
            "description": description_data,
            "user_id": user_id,
            "custom_fields": {
                "12": 16
            }
        }

        response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    ticket_id = response.json()['data']['id']

    if ticket_id:
        await set_ticket(telegram_id, ticket_id, chat_id)
            
        return ticket_id
    else:
        return None