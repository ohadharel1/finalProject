from flask import Flask
from flask_socketio import SocketIO, send
import time
import config
import web_app_client_handler
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['DEBUG'] = False
socketio = SocketIO(app)
# app.run(threaded = True)
handler = web_app_client_handler.WebAppClientHandler()


def send_msg(msg):
    global socketio
    try:
        socketio.emit('my_msg', {'msg': msg})
    except Exception, e:
        print 'send exception: ' + str(e)

@socketio.on('message')
def handleMessage(msg):
    global handler
    print 'got msg: ' + str(msg)
    res = handler.handle_msg(msg)
    if res is not None:
        try:
            send(res, broadcast = False)
        except Exception, e:
            print 'send exception: ' + str(e)

def start_server():
    global socketio
    socketio.run(app)


