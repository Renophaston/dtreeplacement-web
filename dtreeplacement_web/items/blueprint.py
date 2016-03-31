from flask import Blueprint, render_template, redirect, url_for, request
from models import Item, Membership
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
    # list to hold all the Items of which this Item is a "member"
    groups = []
    # find all rows in Membership table that match this item in member_id
    for membership in Membership.query.filter(Membership.member_id == item_id):
        group_id = membership.group_id
        groups.append(Item.query.filter(Item.id == group_id).first())
    return render_template(
        'items/item_detail.j2',
        item=item,
        groups=groups)


@items.route('/add', methods=['GET', 'POST'])
def add():
    # if we're getting POST data, add the new entry
    if request.method == 'POST':
        form = ItemForm(request.form)
        if form.validate():
            # create an Item and fill it with the form data
            # (remember, the groups aren't accounted for here)
            item = Item(form.content.data)
            db.session.add(item)
            db.session.commit()

            # then add the appropriate entries in the membership table
            for group in form.groups.data:
                # print("group: {}".format(group))
                membership = Membership(group, item.id)
                db.session.add(membership)
            db.session.commit()

            # then redirect to the item detail for the added item
            return redirect(url_for('items.item_detail', item_id=item.id))
        else:
            # todo: something better
            print("form didn't validate")
            print(form.errors)

    # otherwise show the add item form
    else:
        form = ItemForm()

    return render_template('items/add.j2', form=form)


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/item_detail.j2', item=None), 404
