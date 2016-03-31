"""Database model definitions."""

# from app, this is the SQLAlchemy object instance
from app import db
import datetime


class Item(db.Model):
    """Describes an item in our non-tree, ie 'Superman #235'."""
    # id, primary key
    id = db.Column(db.Integer, primary_key=True)
    # the content of the item, like a book title, currently just a string
    content = db.Column(db.Text, unique=True, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Item: {}>'.format(self.content)


class Membership(db.Model):
    """Connects an Item to another Item in a group-member relation."""
    # id, primary key
    id = db.Column(db.Integer, primary_key=True)
    # id of Item acting as group/parent
    group_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    # id of Item acting as member/child
    member_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    # only include a relationship in this table once
    __table_args__ = (
        db.UniqueConstraint(group_id, member_id),
    )

    def __init__(self, group_id, member_id):
        self.group_id = group_id
        self.member_id = member_id

    def __repr__(self):
        return '<Membership: item {0} is in group {1}>'.format(
            self.member_id,
            self.group_id
        )
