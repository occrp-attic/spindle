from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from spindle.core import assets, create_app
from spindle.api.base import base_api
from spindle.api.auth import auth_api


def configure_app(config={}):
    app = create_app(config)
    app.register_blueprint(base_api)
    app.register_blueprint(auth_api)
    return app


def main():
    app = configure_app()
    manager = Manager(app)
    manager.add_command('assets', ManageAssets(assets))
    manager.run()


if __name__ == "__main__":
    main()
