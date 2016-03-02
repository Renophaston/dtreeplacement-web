"""Generate database from code in models.py."""

import os, sys
from app import db


sys.path.append(os.getcwd())


if __name__ == '__main__':
    db.create_all()
