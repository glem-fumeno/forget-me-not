from flask import Flask

from api.docs.endpoints import blueprint
from api.users.endpoints import endpoints as users
from api.items.endpoints import endpoints as items
from api.carts.endpoints import endpoints as carts
from config import CONFIG

app = Flask(__name__)
app.register_blueprint(blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(items.blueprint)
app.register_blueprint(carts.blueprint)


if __name__ == "__main__":
    app.run(host=CONFIG["HOST"], port=CONFIG["PORT"], debug=True)
