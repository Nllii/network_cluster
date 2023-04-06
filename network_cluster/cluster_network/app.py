import os
import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import subprocess
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

user = os.path.expanduser("~")
username = user.split('/')[-1]
chat_history_file = 'chat_history.json'



class Command:
    def __init__(self,command):
        self.command = command
        
    
    
    def run(self):
        self.output = subprocess.run(self.command,shell=True,capture_output=True)
        print(self.output)
        return self.output
    
    
    
class Client:
    def __init__(self, username):
        # check if username is {{ username }}
        self.username = f'{username}: '


clients = {}

def get_chat_history():
    if os.path.isfile(chat_history_file):
        with open(chat_history_file, 'r') as f:
            return json.load(f)
        
        
        
    return {'messages': []}

def save_chat_history(chat_history):
    with open(chat_history_file, 'w') as f:
        json.dump(chat_history, f)

chat_history = get_chat_history()

@app.route('/')
def index():
    return render_template('index.html', username=username)

@socketio.on('join')
def join(data):
    # print(data['username'])
    client = Client(data['username'])
    clients[request.sid] = client
    emit('add_user', {'name': client.username}, broadcast=True)
    history = 0
    for message in chat_history['messages']:
        # get the last 5 messages
        history += 1
        if history > len(chat_history['messages']) - 5:
            emit('chat_message', message)

@socketio.on('send_message')
def send_message(data):
    message = {'name': clients[request.sid].username, 'message': data['message']}
    chat_history['messages'].append(message)
    last_message = chat_history['messages'][-1]['message']
    if last_message.startswith("$"):
        # remove the $ sign
        message = last_message[1:]
        command = Command(message)
        output = command.run().stdout.decode('utf-8')
        response = {'name': 'executed response: ', 'message': output}
        chat_history['messages'].append(response)
        save_chat_history(chat_history)
        emit('chat_message', response, broadcast=True)
    else:
        print("command not detected")
    emit('chat_message', message, broadcast=True)

@socketio.on('leave')
def leave():
    client = clients.pop(request.sid, None)
    if client:
        emit('remove_user', {'name': client.username}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    client = clients.pop(request.sid, None)
    if client:
        emit('remove_user', {'name': client.username}, broadcast=True)

def supervisor(DEBUG,PORT):
    socketio.run(app, debug=DEBUG,port=PORT)
    # if __name__ == '__main__':
