from sqlalchemy import Column, Unicode, Enum, Boolean, ForeignKey
from loom.db.util import Base, CommonColumnsMixin


class Permission(Base, CommonColumnsMixin):
    """ A set of rights granted to a role on a resource. """
    __tablename__ = 'permission'

    COLLECTION = 'collection'
    SOURCE = 'source'
    RESOURCE_TYPES = [COLLECTION, SOURCE]

    SYSTEM_GUEST = 'guest'
    SYSTEM_USER = 'user'

    role_id = Column(Unicode, ForeignKey('role.id'), index=True)
    read = Column(Boolean, default=False)
    write = Column(Boolean, default=False)
    resource_id = Column(Unicode, nullable=True)
    resource_type = Column(Enum(*RESOURCE_TYPES, name='permission_type'),
                           nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role_id,
            'read': self.read,
            'write': self.email,
            'resource_id': self.resource_id,
            'resource_type': self.resource_type
        }
