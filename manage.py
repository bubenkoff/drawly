"""Management entry point script."""
from flask.ext.script import Manager, Server

from drawly.app import app, assets

manager = Manager(app)

app.config['DEBUG'] = True

manager.add_command('runserver', Server(host="0.0.0.0", port=8000))

from flask.ext.assets import ManageAssets
manager = Manager(app)

manager.add_command("assets", ManageAssets(assets))

if __name__ == "__main__":
    manager.run()
