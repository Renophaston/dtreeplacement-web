import wtforms
from models import Item


class ItemForm(wtforms.Form):
    content = wtforms.StringField('Content')
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will be a search box w/ autocomplete
        # fixme: item list doesn't update when items are added!
        # choices=([(item.id, item.content) for item in all_items]),
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

    def populate_item(self, item):
        self.populate_obj(item)
        # TODO: add the groups
        return item
