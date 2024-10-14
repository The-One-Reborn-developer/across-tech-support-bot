import os
import sys
import aiohttp
import re

from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv

from app.tasks.celery import get_ticket_task

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(find_dotenv())

app = Flask(__name__)

TOKEN = os.getenv('TOKEN')
TELEGRAM_API_URL_SEND_MESSAGE = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
TELEGRAM_API_URL_SEND_PHOTO = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'


def extract_p_tags(text):
    """Extracts text within <p></p> tags."""
    return re.findall(r'<p>(.*?)</p>', text, re.DOTALL)


def extract_image_url(text):
    """Extracts the image URL from <img> tags."""
    img_match = re.search(r'<img src="(.*?)"', text)
    return img_match.group(1) if img_match else None


@app.route('/', methods=['POST'])
async def ticket_answer_handler() -> None:
    try:
        data = request.get_json()

        print(data)

        ticket_id = data['answer_to_ticket']['ticketID']

        print(ticket_id)

        result = get_ticket_task.delay(ticket_id)

        ticket_id_database = result.get()

        if ticket_id_database:
            chat_id = ticket_id_database[2]

            if chat_id:
                text = data['answer_to_ticket']['text']
                author = data['answer_to_ticket']['author']

                # Extract <p></p> tags and join them into one string
                p_tag_texts = extract_p_tags(text)
                full_text = '\n'.join(p_tag_texts)

                # Extract image URL if any
                image_url = extract_image_url(text)

                # Format the message to be sent to the user
                content = f"Ответ на вашу заявку #{ticket_id} от {author}:\n\n{full_text}"

                # If there's an image, send it with the caption
                if image_url:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            TELEGRAM_API_URL_SEND_PHOTO, 
                            json={
                                'chat_id': chat_id,
                                'photo': image_url,
                                'caption': content,
                                'parse_mode': 'HTML'
                            }
                        ) as response:
                            if response.status != 200:
                                print(f"Failed to send image to chat_id {chat_id}: {await response.text()}")
                                return jsonify({'error': 'Failed to send image'}), 500
                            else:
                                print(f"Image sent to chat_id {chat_id}")
                                return jsonify({'message': 'Image sent successfully'}), 200
                else:
                    # Send the message without the image
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            TELEGRAM_API_URL_SEND_MESSAGE, 
                            json={'chat_id': chat_id, 'text': content, 'parse_mode': 'HTML'}
                        ) as response:
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
    app.run(host='0.0.0.0', port=5000, debug=True)