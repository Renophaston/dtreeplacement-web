from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.j2', title='Test')
