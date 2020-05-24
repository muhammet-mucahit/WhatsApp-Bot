import os
import requests

from datetime import datetime
from flask import Flask, request, jsonify, abort

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

client = Client()

from_whatsapp_number = os.environ.get('FROM_WHATSAPP_NUMBER', '')
to_whatsapp_number = os.environ.get('TO_WHATSAPP_NUMBER', '')


def is_include(arr, message):
    lower_message = message.lower()
    for item in arr:
        'tl' in lower_message


@app.route('/')
def home():
    return jsonify({'success': True})


@app.route('/response_message/', methods=['POST'])
def response_message():
    incoming_message = request.values.get('Body', '')
    response = MessagingResponse()
    outgoing_message = response.message()

    lower_message = incoming_message.lower()
    if 'tl' in lower_message:
        url = 'https://api.frankfurter.app/latest?from=TRY&to=USD,EUR'
        r = requests.get(url)
        if r.status_code == 200:
            body = r.json()
        else:
            body = 'I could not retrieve currencies at this time, sorry.'
    elif 'tarih' in lower_message or 'saat' in lower_message:
        now = datetime.now()
        body = now.strftime("| %d-%m-%Y | %H:%M |")
    else:
        body = "I can't answer this message!"

    outgoing_message.body(body)
    return str(response)


@app.route('/send_message/', methods=['POST'])
def send_message():
    body = request.get_json()

    if body is None or 'message' not in body:
        abort(400)

    try:
        message = body['message']
        message = client.messages.create(body=message,
                                         from_=from_whatsapp_number,
                                         to=to_whatsapp_number)
        return jsonify({
            'success': True,
            'message': message.sid
        })
    except:
        abort(422)


if __name__ == '__main__':
    app.run()
