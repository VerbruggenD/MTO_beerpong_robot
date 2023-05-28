from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from flask_cors import CORS
from flask_bootstrap import Bootstrap
import logging
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['CLIENT_ID'] = 'Rocky'
app.config['log'] = False

# Disable logging of access logs
log = logging.getLogger('werkzeug')
log.propagate = False
log.setLevel(logging.ERROR)
log.addHandler(logging.StreamHandler(sys.stdout))

cors = CORS(app, resources={r"*": {"origins": "*"}})

bootstrap = Bootstrap(app)
socketio = SocketIO(app, logger=False, engineio_logger=False,cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    command = data
    distance = 0
    output_str = f"{command} {int(distance)}"
    print(output_str, flush=True)

@socketio.on('json')
def handle_json(data):
    try:
        json_data = json.loads(data)
        command = json_data['command']
        distance = json_data['distance']
        output_str = f"{command} {int(distance)}"
        print(output_str, flush=True)
    except ValueError as e:
        # code for handling invalid JSON data
        print('Invalid JSON data: {}'.format(data))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, use_reloader=False, debug=False)