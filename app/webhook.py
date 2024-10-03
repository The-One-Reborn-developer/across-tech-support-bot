from flask import Flask, request
import os
import aiohttp
import asyncio

from dotenv import load_dotenv, find_dotenv

from app.database.requests import get_ticket


load_dotenv(find_dotenv())

app = Flask(__name__)

TOKEN = os.getenv('TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


@app.route('/', methods=['POST'])
async def ticket_answer_handler() -> None:
    data = request.get_json()

    ticket_id = data['answer_to_ticket']['ticketID']

    print(ticket_id)

    ticket_id_database = await get_ticket(ticket_id)

    if ticket_id_database:
        chat_id = ticket_id_database[2]

        if chat_id:
            text = data['answer_to_ticket']['text']
            author = data['answer_to_ticket']['author']

            # Format the message to be sent to the user
            content = f"Ответ на вашу заявку #{ticket_id} от {author}:\n\n{text}"

            # Send the message to the chat
            async with aiohttp.ClientSession() as session:
                async with session.post(TELEGRAM_API_URL, json={'chat_id': chat_id, 'text': content}) as response:
                    if response.status != 200:
                        print(f"Failed to send message to chat_id {chat_id}: {await response.text()}")
                    else:
                        print(f"Message sent to chat_id {chat_id}")
                
        else:
            print(f"Chat ID not found for ticket ID {ticket_id}")

    else:
        print(f"Ticket ID {ticket_id} not found in the database")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)