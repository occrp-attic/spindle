from jsonmapping import SchemaVisitor

from spindle import authz
from spindle.core import get_loom_config
from spindle.util import result_entity, OrderedDict


def collection_entities(collection, depth=2, filter_schema=None):
    config = get_loom_config()
    # FIXME: this is a performance nightmare. Think about how to fix it.
    results = []
    q = config.entities.subjects(schema=filter_schema,
                                 collection_id=collection.id,
                                 right=authz.entity_right())
    for (subject, schema) in q:
        data = config.entities.get(subject, schema=schema, depth=depth,
                                   right=authz.entity_right())
        results.append(result_entity(data))
    return results


def entities_to_table(schema, entities):
    """ Generate a flattened table from a set of entities, inlining
    inline sub-entities. """
    config = get_loom_config()
    visitor = SchemaVisitor({'$ref': schema}, config.resolver)
    rows = []
    for entity in entities:
        row = OrderedDict()
        for prop in visitor.properties:
            if prop.is_value and prop.inline:
                row[prop.title] = entity.get(prop.name)
            if prop.is_object:
                child_entity = entity.get(prop.name, {})
                if prop.inline:
                    for child_prop in prop.properties:
                        if not prop.inline:
                            continue
                        title = '%s: %s' % (prop.title, child_prop.title)
                        row[title] = child_entity.get(child_prop.name)
                else:
                    row[prop.title] = child_entity.get('name',
                                                       child_entity.get('id'))
        rows.append(row)
    return visitor, rows
