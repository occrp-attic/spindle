from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from schwifty.core import assets
from schwifty.endpoints import app


manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))


def main():
    manager.run()


if __name__ == "__main__":
    main()
