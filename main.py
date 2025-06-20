from flask import Flask

from api.docs.endpoints import blueprint
from api.users.endpoints import endpoints as users
from config import CONFIG

app = Flask(__name__)
app.register_blueprint(blueprint)
app.register_blueprint(users.blueprint)


if __name__ == "__main__":
    app.run(host=CONFIG["HOST"], port=CONFIG["PORT"], debug=True)
