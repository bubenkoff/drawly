"""App entry point."""
import os.path

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.socketio import SocketIO, emit, join_room, leave_room

from . import canvas

app = Flask(__name__)
assets = Environment(app)

socketio = SocketIO(app)

project_path = os.path.dirname(os.path.dirname(__file__))

# Tell flask-assets where to look for our coffeescript and sass files.
assets.load_path = [
    os.path.join(project_path, 'bower_components'),
    os.path.join(project_path, 'node_modules'),
    os.path.join(os.path.dirname(__file__), 'js'),
    os.path.join(os.path.dirname(__file__), 'css'),
]

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.min.js',
        'drawingboard.js/dist/drawingboard.min.js',
        'canvas.js',
        output='js_all.js'
    )
)

assets.register(
    'css_all',
    Bundle(
        'uikit/css/uikit.min.css',
        'drawingboard.js/dist/drawingboard.min.css',
        'drawly.css',
        output='css_all.css'
    )
)

app.register_blueprint(canvas.blueprint)

USERS = set()


@socketio.on('message')
def handle_message(message):
    emit('message', {
        'message': 'ping'
    })


@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = 'room'
    join_room(room)
    USERS.add(username)
    emit('users', {'users': sorted(USERS)}, room=room)


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = 'room'
    leave_room(room)
    if username in USERS:
        USERS.remove(username)
    emit('users', {'users': sorted(USERS)}, room=room)


@socketio.on('event')
def handle_event(data):
    emit('broadcast_event', data, room='room')
