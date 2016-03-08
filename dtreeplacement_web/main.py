"""Main entry point; starts the server."""

from app import app, db
import views  # routes, etc
import models  # database models

from items.blueprint import items
app.register_blueprint(items, url_prefix='/items')

# only start if this script is being run explicitly
if __name__ == '__main__':
    app.run()
