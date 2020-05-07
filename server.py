from datetime import datetime
import time
from flask import Flask, request, abort

app = Flask(__name__)

messages = []
users = {}


@app.route("/")
def hello():
    return "Welcome to home page!"


@app.route("/status")
def status():
    return {
        'all_users': len(users),
        'all_messages': len(messages),
        'status': True,
        'name': 'MyMess',
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }


@app.route("/send", methods=['POST'])
def send():
    username = request.json['username']
    password = request.json['password']

    if username in users:
        if password != users[username]:
            return abort(401)
    else:
        users[username] = password

    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)

    print(messages)

    return {"ok": True}


@app.route("/messages")
def messages_view():
    after = float(request.args.get('after'))

    filtered_messages = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered_messages
    }


app.run()
