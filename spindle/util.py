import os
from flask import current_app
from flask import url_for as flask_url_for

from spindle import authz


def angular_templates():
    partials_dir = os.path.join(current_app.static_folder, '..')
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
        if current_app.config.get('PREFERRED_URL_SCHEME'):
            kw['_scheme'] = current_app.config.get('PREFERRED_URL_SCHEME')
        return flask_url_for(*a, **kw)
    except RuntimeError:
        return None


def result_entity(entity):
    if '_source' in entity and '_id' in entity:
        entity['_source']['id'] = entity['_id']
        entity = entity['_source']
    entity['$uri'] = url_for('entities.view', id=entity.get('id'))
    colls = entity.get('$collections', [])
    entity['$collections'] = authz.collections(authz.READ).intersection(colls)
    sources = entity.get('$sources', [])
    entity['$sources'] = authz.sources(authz.READ).intersection(sources)
    entity.pop('$text', None)
    entity.pop('$latin', None)
    for k, v in entity.items():
        if isinstance(v, (set, list, tuple)) and len(v) == 0:
            entity.pop(k)
    return entity
