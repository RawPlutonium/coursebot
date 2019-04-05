from flask import Flask, request
import json

PAT = 'EAAEHUFnKtU4BALdtoWbn1RUoMIl7KmZBIfjzd1HmpZA0sQBbsyZBa8G2O7e90h6hia5w6H2PCZAEgBOvcRZBzqMkx19I3FKBV5JqgndPaVorjrnOnY84DjYXZAxkRSTLlX55df8mraAFpZAxWZC4ZAyoUcflqlPxaBL9YPvAkQWEZCsgZDZD'
app = Flask(__name__)
fb_url = 'https://graph.facebook.com/v2.6/me/messages'

@app.route('/verify', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == '90293':
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def message_handler():
    print "Handling messages"
    payload = request.get_data()
    print payload
    for sender, message in message_events(payload):
        print "Incoming message from %s %s" % (sender, message)
        send_message(PAT, sender, message)
    return "ok"

def message_events(payload):
    """generates tuples of (sender_id, message_text) from the provided payload"""
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"

def send_message(token, recipient, text):
    """sends the message text to recipient with id recipient"""
    r = requests.post(fb_url,
        params={"access_token": token},
        data=json.dumps(
        {
        "recipient": {"id":recipient},
        "message": {"text": text.decode('unicode_escape')}
        }),
        headers={'Content-type':'application/json'})
    if r.status_code != requests.codes.ok:
        print r.message_text

if __name__ == '__main__':
    app.run()
