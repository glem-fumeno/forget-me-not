import logging

from flask import Flask
from flask_cors import CORS

from api.carts.endpoints import endpoints as carts
from api.docs.endpoints import blueprint
from api.items.endpoints import endpoints as items
from api.logger import init_logger
from api.users.endpoints import endpoints as users
from config import get_config

init_logger()
config = get_config()

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": config.FRONTEND_URL}},
    supports_credentials=True,
)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
app.register_blueprint(blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(items.blueprint)
app.register_blueprint(carts.blueprint)


if __name__ == "__main__":
    app.run(
        host=config.HOST, port=config.PORT, debug=True, ssl_context="adhoc"
    )
