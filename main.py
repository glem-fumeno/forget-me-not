from flask import Flask

from api.carts.endpoints import endpoints as carts
from api.docs.endpoints import blueprint
from api.items.endpoints import endpoints as items
from api.users.endpoints import endpoints as users
from config import get_config

app = Flask(__name__)
app.register_blueprint(blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(items.blueprint)
app.register_blueprint(carts.blueprint)
config = get_config()


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)
