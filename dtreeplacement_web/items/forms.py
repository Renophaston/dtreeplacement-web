import wtforms
from wtforms.validators import DataRequired
from models import Item, Membership
from helpers import get_items


class ItemForm(wtforms.Form):
    # e.g., "Superman #75"
    content = wtforms.StringField(
        'Content',
        validators=[DataRequired()],
        description='e.g., "Superman #75"'
    )
    # items to select as "parents" for this item
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will be a search box w/ autocomplete
        # choices will get filled in __init__()
        coerce=int,
        description='Select the groups this item should be a member of.'
    )

    def __init__(self, *args, **kwargs):
        wtforms.Form.__init__(self, *args, **kwargs)

        # if we're editing, fill in the existing data
        if 'item' in kwargs:
            item = kwargs['item']
            self.content.data = item.content

            # populate the groups list
            # if we're editing, don't include this item in the list of groups
            all_groups = Item.query\
                .filter(Item.id != item.id, Item.status == Item.STATUS_NORMAL)\
                .order_by(Item.content.asc()).all()

            # the groups that should already be selected on load
            self.groups.data = [group.id for group in item.groups]
        else:
            # only if we're NOT editing an existing item
            # populate the groups list
            all_groups = get_items()

        # populate the groups list
        self.groups.choices = \
            [(group.id, group.content) for group in all_groups]
