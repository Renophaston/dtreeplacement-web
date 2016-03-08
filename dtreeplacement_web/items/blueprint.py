from flask import Blueprint
from models import Item

items = Blueprint('items', __name__, template_folder='templates')


@items.route('/')
def index():
    return 'Items index'


@items.route('/<int:item_id>')
def item_detail(item_id):
    return 'Item detail view for item {}.'.format(item_id)
