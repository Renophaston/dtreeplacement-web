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
            # (remember, the groups aren't accounted for right here)
            item = Item(form.content.data)
            db.session.add(item)
            # need to add the item before the Membership table can refer to it
            db.session.commit()

            # then add the appropriate entries in the membership table
            for group in form.groups.data:
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


@items.route('/<item_id>/edit', methods=['GET', 'POST'])
def edit(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    if request.method == 'POST':
        # we received data, so modify the database
        form = ItemForm(request.form, obj=item)
        if form.validate():
            item.content = form.content.data
            db.session.add(item)
            # have to commit this before doing stuff in another table which
            # references this one
            db.session.commit()

            # change the membership table
            # todo: this just removes all the memberships this item has, then
            # adds back the new set of memberships; it could be more efficient
            existing_memberships = Membership.query.filter(
                Membership.member_id == item_id)
            new_memberships = [Membership(group_id, item_id)
                               for group_id in form.groups.data]

            # add the new memberships to the database
            for existing_membership in existing_memberships:
                db.session.delete(existing_membership)
            db.session.add_all(new_memberships)

            # commit the changes to the database
            db.session.commit()

            # then redirect to the item_detail for the changed item
            return redirect(url_for('items.item_detail', item_id=item.id))
        else:
            # todo: something better
            print("form didn't validate")
            print(form.errors)
    else:
        # we didn't receive data, so display the form
        form = ItemForm(item=item)

    return render_template('items/edit.j2', item=item, form=form)


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/item_detail.j2', item=None), 404
