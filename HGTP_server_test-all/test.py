from flask import Flask
import socket
from flask_socketio import SocketIO,emit
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import time
app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app)
@socketio.on('request_for_response',namespace='/testnamespace')
def give_response(data):
    value = data.get('data')
    print(data)
    if request.headers.get('X-Real-IP') == '127.0.0.1':
       ip = '192.168.18.129'
    if ip not in current_app.config:
        current_app.config[ip]='null'
    print((current_app.config[ip]))
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.18.129', 8065))
        s.sendall('get_jiekou_tiaoshi')
        s.recv(1024)
        s.sendall(ip)
        b = s.recv(1024)
        if b!=current_app.config[ip]:
            print((333333333333333333333333333333))
            current_app.config[ip]=b
            print((current_app.config[ip]))
            print(b)
            emit('response', {'re': b})
            break
        else:
            emit('response', {'re': 'no change'})
if __name__ == '__main__':
     socketio.run(app, debug='False', host='0.0.0.0', port=5000)

