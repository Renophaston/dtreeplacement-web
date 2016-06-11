"""Database model definitions."""

# from app, this is the SQLAlchemy object instance
from app import db
import datetime


# Connects an Item to another Item in a group-member relation.
# http://docs.sqlalchemy.org/en/rel_0_9/orm/join_conditions.html#self-referential-many-to-many
memberships = db.Table(
    'memberships',
    db.Column('group_id', db.Integer, db.ForeignKey('item.id'),
              primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('item.id'),
              primary_key=True),
    # don't let an Item be a member of a group more than once
    db.UniqueConstraint('group_id', 'member_id', name='MemberOnceOnly'),
    # don't let an Item be a member of itself
    db.CheckConstraint('group_id != member_id', name='MemberOfItself')
)


class Item(db.Model):
    """Describes an item in our non-tree, ie 'Superman #235'."""

    # the table name in the database
    __tablename__ = 'item'

    # potential statuses (just whether it's been deleted or not, currently)
    STATUS_NORMAL = 0
    STATUS_DELETED = 1

    # id, primary key
    id = db.Column(db.Integer, primary_key=True)

    # the content of the item, like a book title, currently just a string
    content = db.Column(db.Text, unique=True, nullable=False)

    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    # when this item was last modified
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    # see valid statuses at the top of Item()
    status = db.Column(db.SmallInteger, default=STATUS_NORMAL)

    # helpers to affect changes in membership table
    # members is a list of all Items that are "members" of this Item
    members = db.relationship(
        'Item',
        secondary=memberships,
        primaryjoin=id==memberships.c.group_id,
        secondaryjoin=id==memberships.c.member_id,
        backref='group'
    )

    # groups is a list of all Items of which this Item is a member
    groups = db.relationship(
        'Item',
        secondary=memberships,
        primaryjoin=id==memberships.c.member_id,
        secondaryjoin=id==memberships.c.group_id,
        backref='member'
    )

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Item: {}>'.format(self.content)
