import socketio
import os

sio = socketio.Client()
sio.connect('http://localhost:5001')
user = os.path.expanduser("~")
username = user.split('/')[-1]
PULL = []

@sio.on('connect')
def on_connect():
    print('Connected to server')

@sio.on('chat_message')
def on_chat_message(data):
    if 'name' in data:
        print(f'Received message from : {data["name"]} : $ {data["message"]}')
        if PULL:
            print('Polling server for messages')
        else:
            sio.wait()
            sio.disconnect()

        return data
    else:
        print(f'Executed command successfully --${data}')
        if PULL:
            print('')
        else:
            # sio.wait()
            sio.disconnect()
     

def join_server(username=None):
    sio.emit('join', {'username': f'{username}'})
    

def send_message(message=None):
    sio.emit('join', {'username': f'{username}'})
    sio.emit('send_message', {'message': f'{message}'})



def poll_server(message,pull):
    if pull:
        PULL.append(pull)
    sio.emit('join', {'username': f'{username}'})
    sio.emit('send_message', {'message': f'{message}' ,'pull':pull})


    


