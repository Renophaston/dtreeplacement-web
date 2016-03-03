"""Generate database from code in models.py."""

import os, sys
sys.path.append(os.getcwd())  # before import db, so we can see app
from app import db


if __name__ == '__main__':
    db.create_all()
