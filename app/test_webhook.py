import requests


URL = "http://localhost:80"


def send():
    json = {
        "answer_to_ticket": {
            "ticketID": "82244",
            "text": "тестовый ответ",
            "author": "Иванов Иван Иванович"
        }
    }

    response = requests.post(URL, json=json)
    print(response.text)


if __name__ == "__main__":
    send()