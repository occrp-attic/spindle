from spindle import authz
from spindle.core import get_loom_config
from spindle.util import result_entity


def collection_entities(collection, depth=2, filter_schema=None):
    config = get_loom_config()
    if filter_schema is not None:
        filter_schema = config.implied_schemas(filter_schema)
    # FIXME: this is a performance nightmare. Think about how to fix it.
    results = []
    for cs in collection.subjects:
        schema = config.entities.get_schema(cs.subject,
                                            right=authz.entity_right())
        if schema is None:
            continue
        if filter_schema is not None and schema not in filter_schema:
            continue
        data = config.entities.get(cs.subject, schema=schema, depth=depth,
                                   right=authz.entity_right())
        results.append(result_entity(data))
    return results
