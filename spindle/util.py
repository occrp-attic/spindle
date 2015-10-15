import os
from flask import url_for as flask_url_for

from spindle.core import app


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


def result_entity(entity):
    if '_source' in entity and '_id' in entity:
        entity = entity['_source']
    entity['$uri'] = url_for('entity', id=entity.get('id'))
    entity.pop('$text', None)
    entity.pop('$latin', None)
    for k, v in entity.items():
        if isinstance(v, (set, list, tuple)) and len(v) == 0:
            entity.pop(k)
    return entity
