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


# @app.route('/item')
# def item_index():
#     items = Item.query.all()
#     return render_template('item.j2', items=items)
#
#
# @app.route('/item/<int:item_id>')
# def item_view(item_id):
#     item = Item.query.filter(Item.id == item_id).first()
#     if item is None:
#         message = 'No fucking items matching id {}.'.format(item_id)
#     else:
#         message = 'Item {}: {}'.format(item_id, item.content)
#     return render_template(
#         'index.j2',
#         title='Item',
#         message=message
#     )
