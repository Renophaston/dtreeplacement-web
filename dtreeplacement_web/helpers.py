from models import Item


# helper to retrieve all non-deleted items
def get_items(include_deleted=False):
    if include_deleted:
        return Item.query.order_by(Item.content.asc()).all()

    return Item.query.filter(Item.status == Item.STATUS_NORMAL)\
        .order_by(Item.content.asc())\
        .all()


# helper to retrieve just the deleted items
def get_deleted_items():
    return Item.query.filter(Item.status == Item.STATUS_DELETED)\
        .order_by(Item.content.asc())\
        .all()
