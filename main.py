from flask import Flask

from api.docs.endpoints import docs
from api.users.endpoints import users
from config import CONFIG

app = Flask(__name__)
app.register_blueprint(docs)
app.register_blueprint(users)


if __name__ == "__main__":
    app.run(host=CONFIG["HOST"], port=CONFIG["PORT"], debug=True)
