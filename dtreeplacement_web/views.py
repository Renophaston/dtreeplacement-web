"""Views and routes for the UI."""

from app import app, db
from flask import render_template
from models import Item


@app.route('/')
def index():
    items = Item.query.all()
    return render_template(
        'index.j2',
        title='Index',
        message='Welcome.',
        items=items
    )


@app.route('/createtables')
def create_tables():
    db.create_all()
    return render_template(
        'index.j2',
        title='Index',
        message='ATTEMPTED to create tables, anyway.'
    )


@app.route('/item')
def item_index():
    items = Item.query.all()
    return render_template('item.j2', items=items)


@app.route('/item/<int:item_id>')
def item_view(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    if item is None:
        message = 'No fucking items matching id {}.'.format(item_id)
    else:
        message = 'Item {}: {}'.format(item_id, item.content)
    return render_template(
        'index.j2',
        title='Item',
        message=message
    )
