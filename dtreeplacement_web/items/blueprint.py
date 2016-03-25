from flask import Blueprint, render_template, redirect, url_for, request
from models import Item
from items.forms import ItemForm
from app import db

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    all_items = Item.query.order_by(Item.content.asc()).all()
    return render_template('items/index.j2', items=all_items)


@items.route('/<int:item_id>')
def item_detail(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    return render_template('items/item_detail.j2', item=item)


@items.route('/add', methods=['GET', 'POST'])
def add():
    # if we're getting POST data, add the new entry
    if request.method == 'POST':
        form = ItemForm(request.form)
        if form.validate():
            item = form.save_item(Item())
            db.session.add(item)
            db.session.commit()
            # then redirect to the item detail for the added item
            return redirect(url_for('items.item_detail', item_id=item.id))
    # otherwise show the add item form
    else:
        form = ItemForm()
    return render_template('items/add.j2', form=form)


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/item_detail.j2', item=None), 404
