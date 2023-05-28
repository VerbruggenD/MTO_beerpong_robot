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

up_cmd = [1]
down_cmd = [2]
left_cmd = [3]
right_cmd = [4]
start_cmd = [5]
stop_cmd = [6]
retract_cmd = [7]
shoot_cmd = [8]

value = [0]
hor_steps = [200]
vertical_steps = [200]
retract_steps = [200]

PIPE_NAME = "cmd_pipe"

@app.before_first_request
def setup():

    if not os.path.exists(PIPE_NAME):
         os.mkfifo(PIPE_NAME)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):

    fifo = open(PIPE_NAME, 'wb')

    if data == 'UP':
        # code for moving the robot up
        message = bytes(up_cmd + vertical_steps)
        print('Moving robot up')
        fifo.write(message)
    elif data == 'DOWN':
        # code for moving the robot down
        print('Moving robot down')
        message = bytes(down_cmd + vertical_steps)
        fifo.write(message)
    elif data == 'LEFT':
        # code for moving the robot left
        print('Moving robot left')
        message = bytes(left_cmd + hor_steps)
        fifo.write(message)
    elif data == 'RIGHT':
        # code for moving the robot right
        print('Moving robot right')
        message = bytes(right_cmd + hor_steps)
        fifo.write(message)
    elif data == 'START':
        # code for starting auto mode
        print('Starting auto mode')
        message = bytes(start_cmd + [0])
        fifo.write(message)
    elif data == 'STOP':
        # code for stopping all operations
        print('Stopping all operations')
        message = bytes(stop_cmd + [0])
        fifo.write(message)
    else:
        # code for handling unknown command
        print('Unknown command: {}'.format(data))

    fifo.close()

@socketio.on('json')
def handle_json(data):
    fifo = open(PIPE_NAME, 'wb')
    try:
        json_data = json.loads(data)
        command = json_data['command']
        distance = json_data['distance']
        if command == 'FIRE':
            # code for firing the robot with the given distance
            print('Firing robot with distance: {}'.format(distance))
            message = bytes(shoot_cmd + [distance])
            fifo.write(message)
        else:
            # code for handling unknown command
            print('Unknown command: {}'.format(command))
    except ValueError as e:
        # code for handling invalid JSON data
        print('Invalid JSON data: {}'.format(data))
        
    fifo.close()


if __name__ == '__main__':
    setup()
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, debug=True)