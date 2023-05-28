from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import os
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['CLIENT_ID'] = 'Rocky'

cors = CORS(app, resources={r"*": {"origins": "*"}})

bootstrap = Bootstrap(app)
socketio = SocketIO(app,cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    if data == 'UP':
        # code for moving the robot up
        print('Moving robot up')
    elif data == 'DOWN':
        # code for moving the robot down
        print('Moving robot down')
    elif data == 'LEFT':
        # code for moving the robot left
        print('Moving robot left')
    elif data == 'RIGHT':
        # code for moving the robot right
        print('Moving robot right')
    else:
        # code for handling unknown command
        print('Unknown command: {}'.format(data))

@socketio.on('json')
def handle_json(data):
    try:
        json_data = json.loads(data)
        command = json_data['command']
        distance = json_data['distance']
        if command == 'FIRE':
            # code for firing the robot with the given distance
            print('Firing robot with distance: {}'.format(distance))
        else:
            # code for handling unknown command
            print('Unknown command: {}'.format(command))
    except ValueError as e:
        # code for handling invalid JSON data
        print('Invalid JSON data: {}'.format(data))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, debug=True)