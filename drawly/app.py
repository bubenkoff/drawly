"""App entry point."""
import os.path

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask_sockets import Sockets

from . import canvas

app = Flask(__name__)
assets = Environment(app)

sockets = Sockets(app)

project_path = os.path.dirname(os.path.dirname(__file__))

# Tell flask-assets where to look for our coffeescript and sass files.
assets.load_path = [
    os.path.join(project_path, 'bower_components'),
    os.path.join(os.path.dirname(__file__), 'js'),
    os.path.join(os.path.dirname(__file__), 'css'),
]

assets.register(
    'js_all',
    Bundle(
        'jquery/dist/jquery.min.js',
        'drawingboard.js/dist/drawingboard.min.js',
        'sockjs-client/dist/sockjs.js',
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


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)
