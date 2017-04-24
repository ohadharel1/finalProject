from flask import Flask
from flask_socketio import SocketIO, send
import time
import config
import web_app_client_handler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SERVER_NAME'] = config.local_address + ':5000'
# app.config['DEBUG'] = True
socketio = SocketIO(app)
handler = web_app_client_handler.WebAppClientHandler()


def send_msg(msg):
    global socketio
    print('my_msg: ' + str(msg))
    socketio.emit('my_msg', {'msg': msg})

@socketio.on('message')
def handleMessage(msg):
    global handler
    print('Message: ' + str(msg))
    res = handler.handle_msg(msg)
    if res is not None:
        send(res, broadcast = False)

def start_server():
    global socketio
    socketio.run(app)


