from flask import Blueprint, render_template
from models import Item
from items.forms import ItemForm

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    all_items = Item.query.order_by(Item.content.asc()).all()
    return render_template('items/index.j2', items=all_items)


@items.route('/<int:item_id>')
def item_detail(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    return render_template('items/item_detail.j2', item=item)


@items.route('/add')
def add():
    form = ItemForm()
    return render_template('items/add.j2', form=form)


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/item_detail.j2', item=None), 404
