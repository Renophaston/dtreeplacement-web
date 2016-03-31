import wtforms
from models import Item


class ItemForm(wtforms.Form):
    # e.g., "Superman #75"
    content = wtforms.StringField('Content')
    # items to select as "parents" for this item
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will be a search box w/ autocomplete
        # choices will get filled in __init__()
        choices=[],
        coerce=int
    )

    def __init__(self, *args, **kwargs):
        # populate the groups list
        all_items = Item.query.order_by(Item.content.asc()).all()
        self.groups.kwargs['choices'] =\
            [(item.id, item.content) for item in all_items]
        wtforms.Form.__init__(self, *args, **kwargs)
