import base64
import os
import requests

from dotenv import load_dotenv, find_dotenv


async def get_ticket_status(ticket_id: int) -> list | None:
    load_dotenv(find_dotenv())
    
    url = f'https://helpdesk.across.ru/api/v2/tickets/{ticket_id}'

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

    ticket_status = response.json()['data']['deleted']
    ticket_sla = response.json()['data']['sla_date']

    ticket_status_data = [ticket_status, ticket_sla]

    return ticket_status_data