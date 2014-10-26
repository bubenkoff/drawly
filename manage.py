"""Management entry point script."""
from flask.ext.script import Manager, Server
from flask.ext.assets import ManageAssets

from drawly.app import app, assets, socketio

manager = Manager(app)

app.config['DEBUG'] = True


class Runserver(Server):

    def __call__(self, app, host, port, **kwargs):
        socketio.run(app, host=host, port=port)

manager.add_command('runserver', Runserver(app))


class CollectStaticAssets(ManageAssets):
    """Emulate django collectstatic."""

    def run(self, args):
        super(CollectStaticAssets, self).run(['build'])


manager.add_command("collectstatic", CollectStaticAssets(assets))

if __name__ == "__main__":
    manager.run()
