from sqlalchemy import Column, Unicode, Boolean, Enum
from sqlalchemy.orm import relationship

from loom.db.util import Base, CommonColumnsMixin, session


class Role(Base, CommonColumnsMixin):
    """ A user, group or other access control subject. """
    __tablename__ = 'role'

    USER = 'user'
    GROUP = 'group'
    SYSTEM = 'system'
    TYPES = [USER, GROUP, SYSTEM]

    SYSTEM_GUEST = 'guest'
    SYSTEM_USER = 'user'

    id = Column(Unicode(512), nullable=False, primary_key=True, unique=True)
    name = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    type = Column(Enum(*TYPES, name='role_type'), nullable=False)
    permissions = relationship("Permission", backref="role")

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_admin': self.is_admin,
            # 'email': self.email,
            'type': self.type
        }

    @classmethod
    def create_defaults(cls):
        cls.load_or_create(cls.SYSTEM_GUEST, cls.SYSTEM, 'All visitors')
        cls.load_or_create(cls.SYSTEM_USER, cls.SYSTEM, 'Logged-in users')

    @classmethod
    def load(cls, id):
        if id is not None:
            return session.query(cls).filter_by(id=id).first()

    @classmethod
    def load_or_create(cls, id, type, name, email=None, is_admin=False):
        role = cls.load(id)
        if role is None:
            role = cls(id, type)
        role.name = name
        role.email = email
        role.is_admin = is_admin
        session.add(role)
        return role
