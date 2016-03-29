import wtforms
from models import Item


class ItemForm(wtforms.Form):
    content = wtforms.StringField('Content')

    # create the list of possible groups to include item in
    all_items = Item.query.order_by(Item.content.asc()).all()
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will list all other nodes for selecting,
        # and after that sometime it will be a search box
        choices=([(item.id, item.content) for item in all_items]),
        coerce=int
    )

    def populate_item(self, item):
        self.populate_obj(item)
        # TODO: add the groups
        return item
