from flask import Blueprint, render_template, redirect, url_for, request
from models import Item, Membership
from items.forms import ItemForm
from app import db
from helpers import get_items, get_deleted_items

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    all_items = get_items()
    deleted_items = get_deleted_items()
    return render_template('items/index.j2', items=all_items,
                           deleted_items=deleted_items)


@items.route('/<int:item_id>')
def item_detail(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    # list to hold all the Items of which this Item is a "member"
    groups = []
    # find all rows in Membership table that match this item in member_id
    for membership in Membership.query.filter(Membership.member_id == item_id):
        group = Item.query.filter(Item.id == membership.group_id,
                                  Item.status == Item.STATUS_NORMAL).first()
        if group is not None:
            groups.append(group)

    return render_template(
        'items/detail.j2',
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
            memberships = [Membership(group_id, item.id)
                           for group_id in form.groups.data]
            db.session.add_all(memberships)
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

            # delete old relationships
            for existing_membership in existing_memberships:
                db.session.delete(existing_membership)
            # if I didn't commit these before adding the new ones, I'd get a
            # uniqueness exception; I guess it doesn't just do this part first
            # by itself
            db.session.commit()

            # add the new memberships to the database
            db.session.add_all(new_memberships)
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


@items.route('/<item_id>/delete', methods=['GET', 'POST'])
def delete(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    if request.method == 'POST':
        item.status = Item.STATUS_DELETED
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('items.index'))

    return render_template('items/delete.j2', item=item)


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/detail.j2', item=None), 404

