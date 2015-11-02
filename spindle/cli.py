from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from spindle.core import assets, create_app, get_loom_indexer
from spindle.api.base import base_api
from spindle.api.auth import auth_api
from spindle.api.entities import entities_api
from spindle.api.collections import collections_api


def configure_app(config={}):
    app = create_app(config)
    app.register_blueprint(base_api)
    app.register_blueprint(auth_api)
    app.register_blueprint(entities_api)
    app.register_blueprint(collections_api)
    return app


def main():
    app = configure_app()
    manager = Manager(app)
    manager.add_command('assets', ManageAssets(assets))

    @manager.command
    def init():
        "Initialize all parts of the system"
        indexer = get_loom_indexer()
        indexer.configure()

    manager.run()


if __name__ == "__main__":
    main()
