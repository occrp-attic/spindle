import os
from flask import url_for as flask_url_for

from schwifty.core import app


def angular_templates():
    partials_dir = os.path.join(app.static_folder, '..')
    partials_dir = os.path.join(partials_dir, 'templates', 'angular')
    for (root, dirs, files) in os.walk(partials_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as fh:
                file_name = file_path[len(partials_dir) + 1:]
                yield (file_name, fh.read().decode('utf-8'))


def url_for(*a, **kw):
    """ Always generate external URLs. """
    try:
        kw['_external'] = True
        return flask_url_for(*a, **kw)
    except RuntimeError:
        return None
