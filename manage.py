"""Management entry point script."""
from flask.ext.script import Manager, Server

from drawly.app import socketio, app

manager = Manager(app)

app.config['DEBUG'] = True

manager.add_command('runserver', Server(host="0.0.0.0", port=8000))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)
