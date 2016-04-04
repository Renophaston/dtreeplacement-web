import wtforms
from wtforms.validators import DataRequired
from models import Item, Membership


class ItemForm(wtforms.Form):
    # e.g., "Superman #75"
    content = wtforms.StringField(
        'Content',
        validators=[DataRequired()],
    )
    # items to select as "parents" for this item
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will be a search box w/ autocomplete
        # choices will get filled in __init__()
        coerce=int,
    )

    def __init__(self, *args, **kwargs):
        wtforms.Form.__init__(self, *args, **kwargs)

        # populate the groups list
        all_groups = Item.query.order_by(Item.content.asc()).all()
        self.groups.choices =\
            [(group.id, group.content) for group in all_groups]

        # if we're editing, fill in the existing data
        if 'item' in kwargs:
            item = kwargs['item']
            self.content.data = item.content
            selected_memberships =\
                Membership.query.filter(Membership.member_id == item.id).all()
            self.groups.data =\
                [membership.group_id for membership in selected_memberships]

