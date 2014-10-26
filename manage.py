"""Management entry point script."""
from flask.ext.script import Manager, Server

from drawly.app import app, assets

manager = Manager(app)

app.config['DEBUG'] = True

manager.add_command('runserver', Server(host="0.0.0.0", port=8000))

from flask.ext.assets import ManageAssets
manager = Manager(app)


class CollectStaticAssets(ManageAssets):
    """Emulate django collectstatic."""

    def run(self, args):
        super(CollectStaticAssets, self).run(['build'])


manager.add_command("collectstatic", CollectStaticAssets(assets))

if __name__ == "__main__":
    manager.run()
