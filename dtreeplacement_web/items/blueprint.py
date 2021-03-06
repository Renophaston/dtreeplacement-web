from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Item
from items.forms import ItemForm
from app import db
from helpers import get_items, get_deleted_items

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    return render_template('items/index.j2', items=get_items(),
                           deleted_items=get_deleted_items())


@items.route('/<int:item_id>')
def detail(item_id):
    # retrieve item
    item = Item.query.filter(Item.id == item_id).first_or_404()

    # todo: filter out deleted items
    return render_template(
        'items/detail.j2',
        item=item,
        groups=item.groups,
        members=item.members
    )


@items.route('/add', methods=['GET', 'POST'])
def add():
    # if we're getting POST data, add the new entry
    if request.method == 'POST':
        form = ItemForm(request.form)
        if form.validate():
            # create an Item and fill it with the form data
            # (remember, the groups aren't accounted for right here)
            item = Item(form.content.data)

            # then add the appropriate memberships
            for group_id in form.groups.data:
                item.members.append(Item.query.get(group_id))

            # commit the changes
            db.session.add(item)
            db.session.commit()

            # then redirect to the item detail for the added item
            flash('Item {} has been added.'.format(item.id), 'info')
            return redirect(url_for('items.detail', item_id=item.id))
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
    # retrieve the item we're going to edit
    item = Item.query.filter(Item.id == item_id).first_or_404()

    if request.method == 'POST':
        # we received data, so modify the database
        form = ItemForm(request.form, obj=item)
        if form.validate():
            # replace the content
            item.content = form.content.data

            # replace the list of groups
            item.groups =\
                [Item.query.get(group_id) for group_id in form.groups.data]

            # commit our changes
            db.session.add(item)
            db.session.commit()

            # then redirect to the detail for the changed item
            flash('Item {} successfully edited.'.format(item.id), 'info')
            return redirect(url_for('items.detail', item_id=item.id))
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
        flash('Item {} successfully deleted.'.format(item.id), 'info')
        return redirect(url_for('items.index'))

    return render_template('items/delete.j2', item=item)


@items.route('/<item_id>/restore', methods=['POST'])
def restore(item_id):
    item = Item.query.filter(Item.id == item_id).first_or_404()
    if item.status == Item.STATUS_DELETED:
        item.status = Item.STATUS_NORMAL
        db.session.add(item)
        db.session.commit()

    # todo: some sort of error reporting is needed here
    flash('Item {} successfully restored.'.format(item.id), 'info')
    return redirect(url_for('items.detail', item_id=item_id))


@items.errorhandler(404)
def item_not_found(error):
    return render_template('items/detail.j2', item=None), 404

