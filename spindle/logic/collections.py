from werkzeug.exceptions import BadRequest
from loom.db import CollectionSubject, session

from spindle.core import get_loom_config


def collection_add_entity(collection, subject):
    q = session.query(CollectionSubject).filter_by(subject=subject)
    q = q.filter_by(collection_id=collection.id)
    cs = q.first()
    if cs is None:
        cs = CollectionSubject(collection, subject)
    session.add(cs)
    session.commit()


def update_subjects(collection, data):
    """ There must be a nicer way to do this in SQLA. """
    # TODO: authz
    subjects = data.get('subjects', [])
    for cs in collection.subjects:
        if cs.subject in subjects:
            subjects.remove(cs.subject)
        else:
            session.delete(cs)
    for subject in subjects:
        if get_loom_config().entities.get_schema(subject):
            cs = CollectionSubject(collection, subject)
            session.add(cs)
        else:
            raise BadRequest()
