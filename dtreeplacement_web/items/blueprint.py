from flask import Blueprint, render_template
from models import Item

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    all_items = Item.query.all()
    return render_template('items/index.j2', items=all_items)


@items.route('/<int:item_id>')
def item_detail(item_id):
    item = Item.query.filter(Item.id == item_id).first()
    return render_template('items/item_detail.j2', item=item)
