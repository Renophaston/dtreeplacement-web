"""Database model definitions."""

# from app, this is the SQLAlchemy object instance
from app import db
import datetime


class Item(db.Model):
    """Describes an item in our non-tree, ie 'Superman #235'."""
    # id, primary key
    id = db.Column(db.Integer, primary_key=True)
    # the content of the item, like a book title, currently just a string
    content = db.Column(db.Text, unique=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    # override constructor if necessary
    # def __init__(self, *args, **kwargs):
    #     # call parent constructor
    #     super(Item, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Item: %s>' % self.content
