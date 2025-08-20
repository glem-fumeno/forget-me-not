import logging

from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS

from api.docs.endpoints import blueprint
from api.endpoints.carts import endpoints as carts
from api.endpoints.items import endpoints as items
from api.endpoints.recipes import endpoints as recipes
from api.logger import init_logger
from config import get_config

init_logger()
config = get_config()

app = Flask(__name__, static_folder="icons", static_url_path="/icons")
CORS(
    app,
    resources={r"/*": {"origins": config.FRONTEND_URL}},
    supports_credentials=True,
)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
app.register_blueprint(blueprint)
app.register_blueprint(items.blueprint)
app.register_blueprint(carts.blueprint)
app.register_blueprint(recipes.blueprint)

asgi = WsgiToAsgi(app)
