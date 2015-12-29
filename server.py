from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
from collections import deque

queue=deque();

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print("User connected!")
    queue.append({'an': {'id': 'n0', 'label': 'n0', 'x': 0, 'y': 0, 'size': 1}})
    queue.append({'an': {'id': 'n1', 'label': 'n1', 'x': 0, 'y': 1, 'size': 1}})
    queue.append({'ae': {'id': 'e1', 'source': 'n1', 'target': 'n0'}})
    queue.append({'an': {'id': 'n2', 'label': 'n2', 'x': 1, 'y': 1, 'size': 1}})
    queue.append({'ae': {'id': 'e2', 'source': 'n1', 'target': 'n2'}})
    queue.append({'ae': {'id': 'e3', 'source': 'n0', 'target': 'n2'}})

@socketio.on('GET')
def handle_message(message):
    if queue:
        data=queue.popleft()
        for key in data:
            emit(key, data[key])
            break
    else:
        emit('none','')

if __name__ == '__main__':
    socketio.run(app)
