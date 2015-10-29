from datetime import datetime

from spindle.core import db


class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Unicode(1024))
    title = db.Column(db.Unicode(1024))
    url = db.Column(db.Unicode())

    def to_dict(self):
        return {
            'slug': self.slug,
            'title': self.title,
            'url': self.url
        }
