import wtforms
from models import Item


class ItemForm(wtforms.Form):
    content = wtforms.StringField('Content')
    groups = wtforms.SelectMultipleField(
        'Groups',
        # eventually this will list all other nodes for selecting,
        # and after that sometime it will be a search box
        choices=(
            (1, 'One'),
            (2, 'Two')),
        coerce=int
    )

    def save_item(self, item):
        self.populate_obj(item)
        # TODO: add the groups
        return item
