"""Views and routes for the UI."""

from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.j2', title='Index', message='Welcome.')


@app.route('/test')
def intext():
    return render_template('index.j2', title='Intext', message='Testing.')
