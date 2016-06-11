"""Views and routes for the UI.

URL scheme I'm thinking about:
/ (index)
/items (all items somehow)
/items/<int:item_id> (one item)

User stuff will come later, and will include stuff like create_tables.
"""

from app import app, db
from flask import render_template


@app.route('/')
def index():
    return render_template('index.j2')


@app.route('/createtables')
def create_tables():
    db.create_all()
    return render_template(
        'index.j2',
        title='Index',
        message='ATTEMPTED to create tables, anyway.'
    )

from models import Item

@app.route('/test')
def test():
    # item1 = Item('first1')
    # item2 = Item('second1')
    # item3 = Item('third1')
    # item1.members.append(item2)
    # item1.members.append(item3)
    # item2.members.append(item1)
    # db.session.add(item1)
    # db.session.add(item2)
    # db.session.add(item3)
    # db.session.add(item2)
    # print(item.groups)
    # item.members.remove(Item.query.get(9))
    # item = Item.query.get(1)
    # item.members.append(item)
    # db.session.add(item)
    # item2 = Item.query.get(2)
    # item2.members.append(Item.query.get(1))
    # db.session.add(item2)
    # item1 = Item.query.get(1)
    # item1.members.append(item1)
    # db.session.commit()

    return render_template('index.j2')
