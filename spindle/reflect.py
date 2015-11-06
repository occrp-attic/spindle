from jsonmapping import SchemaVisitor

from spindle.core import get_loom_config


def prepare_resolver():
    """ Load all schemas specified as well-known. """
    config = get_loom_config()
    for uri in config.schemas.values():
        config.resolver.resolve(uri)
    return config.resolver

def _check_match(visitor, schema_uri):
    if visitor.id == schema_uri:
        return True
    for parent in visitor.inherited:
        if _check_match(parent, schema_uri):
            return True
    return False

def implied_schemas(schema_uri):
    """ Given a schema URI, return a list of implied (i.e. child) schema URIs,
    with the original schema included. """
    resolver = prepare_resolver()
    schemas = [schema_uri]
    for uri, data in resolver.store.items():
        if isinstance(data, dict):
            visitor = SchemaVisitor(data, resolver)
            if _check_match(visitor, schema_uri):
                schemas.append(data.get('id'))
    return schemas
