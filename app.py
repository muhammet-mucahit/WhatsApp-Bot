from datetime import datetime
from flask import Flask, request, jsonify, abort

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client()

# this is the Twilio sandbox testing number
from_whatsapp_number = 'whatsapp:+14155238886'


@app.route('/')
def home():
    return jsonify({'success': True})


@app.route('/response_message/', methods=['POST'])
def response_message():
    incoming_message = request.values.get('Body', '')
    response = MessagingResponse()
    outgoing_message = response.message()

    lower_message = incoming_message.lower()
    if 'canim' in lower_message:
        datetime.now()
    elif 'tarih' in lower_message or 'saat' in lower_message:
        now = datetime.now()
        outgoing_message.body(now.strftime("| %d-%m-%Y | %H:%M |"))
    else:
        outgoing_message.body("I can't answer this message!")

    return str(response)


@app.route('/send_message/', methods=['POST'])
def send_message():
    body = request.get_json()

    if body is None or 'phone_number' not in body or 'message' not in body:
        abort(400)

    try:
        phone_number, message = body['phone_number'], body['message']

        to_whatsapp_number = f'whatsapp:{phone_number}'
        message = client.messages.create(body=message,
                                         from_=from_whatsapp_number,
                                         to=to_whatsapp_number)
        return jsonify({
            'success': True,
            'message': message.sid
        })
    except:
        abort(422)

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
