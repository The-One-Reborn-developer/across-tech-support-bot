import base64, os, requests

from dotenv import load_dotenv, find_dotenv


async def update_ticket(ticket_id: int,
                        text: str,
                        user_id: int,
                        has_photo: bool,
                        telegram_id: int) -> int | None:
    load_dotenv(find_dotenv())
    
    url = f'https://helpdesk.across.ru/api/v2/tickets/{ticket_id}/posts'

    auth_string = f'{os.getenv("EMAIL")}:{os.getenv("API")}'

    encoded_bytes = base64.b64encode(auth_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_string}"
    }

    if has_photo:
        directory_path = f'app/photos/{telegram_id}'
        
        files = []

        payload = {
            "text": text,
            "user_id": user_id
        }

        # Loop through all files in the directory and add them to the files list
        for filename in os.listdir(directory_path):
            # Create the full file path
            file_path = os.path.join(directory_path, filename)

            # Append the file to the files list in the required format
            files.append(
                ('files[]', 
                (filename, open(file_path, 'rb'), 'image/jpeg'))
            )

        response = requests.post(url, headers=headers, data=payload, files=files)
    else:
        payload = {
            "text": text,
            "user_id": user_id
        }

        response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    return response.status_code