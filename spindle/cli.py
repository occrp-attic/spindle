from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from spindle.core import assets, create_app
from spindle.endpoints import base_api


def configure_app(config={}):
    app = create_app(config)
    app.register_blueprint(base_api)
    return app


def main():
    app = configure_app()
    manager = Manager(app)
    manager.add_command('assets', ManageAssets(assets))
    manager.run()


if __name__ == "__main__":
    main()
