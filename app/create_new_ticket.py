import base64, os, requests

from dotenv import load_dotenv, find_dotenv


async def send_request(name: str,
                       position: str,
                       region: str,
                       phone: str,
                       medical_organization: str,
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

    '''
    Status Code: 200
    Response Body: {
        "data":
        {
            "id":79038,
            "pid":0,
            "unique_id":"0000079038",
            "date_created":"2024-08-14 19:10:59",
            "date_updated":"2024-08-14 19:10:59",
            "title":"Telegram bot",
            "source":"api",
            "status_id":"open",
            "priority_id":2,
            "type_id":0,
            "department_id":1,
            "department_name":"Тех. поддержка",
            "owner_id":0,
            "owner_name":"",
            "owner_lastname":"",
            "owner_email":"",
            "user_id":2320,
            "user_name":"Никита",
            "user_lastname":"Цыганков",
            "user_email":"tsygankov.ns@gmail.com",
            "cc":[],
            "bcc":[],
            "followers":[],
            "ticket_lock":0,
            "sla_date":"26.08.2024 19:00",
            "sla_flag":0,
            "freeze_date":null,
            "freeze":0,
            "viewed_by_staff":1,
            "viewed_by_client":0,
            "rate":"",
            "rate_comment":"",
            "rate_date":"",
            "deleted":0,
            "custom_fields":[
                {"id":12,"field_type":"select","field_value":{"id":16,"name":{"ru":"Прочее"}}},
                {"id":9,"field_type":"checkbox","field_value":0},
                {"id":8,"field_type":"checkbox","field_value":0},
                {"id":10,"field_type":"checkbox","field_value":0},
                {"id":13,"field_type":"number","field_value":""},
                {"id":14,"field_type":"checkbox","field_value":0}],
                "tags":[],
                "jira_issues":[]
        }
    }
    '''

    if request_type == "critical":
        request_type_data = "Критическая ошибка ЛИС"
    elif request_type == "no_exchange":
        request_type_data = "Нет обмена с МИС"
    elif request_type == "no_connection":
        request_type_data = "Нет связи с анализаторами"
    elif request_type == "other":
        request_type_data = "Другое"

    description_data = f"Тип заявки: {request_type_data}; " + \
                       f"Описание: {request_description}; " + \
                       f"ФИО заявителя: {name}; " + \
                       f"Регион: {region}; " + \
                       f"Мед. организация: {medical_organization}; " + \
                       f"Должность: {position}; "
    
    user_email_data = f'{phone}@auto.bot'

    payload = {
        "title": "Across-Tex",
        "description": description_data,
        "user_email": user_email_data,
        "custom_fields": {
            "12":16
            }
    }

    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")