import base64, os, requests

from dotenv import load_dotenv, find_dotenv


async def create_ticket(user_id: int,
                        user_region: str,
                        user_position: str,
                        request_type: str,
                        request_description: str) -> None:
    load_dotenv(find_dotenv())

    url = 'https://helpdesk.across.ru/api/v2/tickets'

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}",
        "Content-Type": "application/json"
    }

    if request_type == "critical":
        request_type_data = "Критическая ошибка ЛИС"
    elif request_type == "no_exchange":
        request_type_data = "Нет обмена с МИС"
    elif request_type == "no_connection":
        request_type_data = "Нет связи с анализаторами"
    elif request_type == "other":
        request_type_data = "Другое"

    if user_region == "Belgorod":
        user_region_data = "Белгородская область"

    description_data = f"{request_description}; " + \
                       f"Регион: {user_region_data}; " + \
                       f"Должность: {user_position}; "

    payload = {
        "title": request_type_data,
        "description": description_data,
        "user_id": user_id,
        "custom_fields": {
            "12":16
            }
    }

    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")