from flask import Flask, request, jsonify
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
    try:
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
                    async with session.post(TELEGRAM_API_URL, json={'chat_id': chat_id, 'text': content, 'parse_mode': 'HTML'}) as response:
                        if response.status != 200:
                            print(f"Failed to send message to chat_id {chat_id}: {await response.text()}")
                            return jsonify({'error': 'Failed to send message'}), 500
                        else:
                            print(f"Message sent to chat_id {chat_id}")
                            return jsonify({'message': 'Message sent successfully'}), 200

            else:
                print(f"Chat ID not found for ticket ID {ticket_id}")
                return jsonify({'error': 'Chat ID not found'}), 404

        else:
            print(f"Ticket ID {ticket_id} not found in the database")
            return jsonify({'error': 'Ticket not found'}), 404
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)