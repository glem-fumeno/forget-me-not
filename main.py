from dataclasses import dataclass

from flask import Flask, request

from api.schemas import Request, Response
from api.docs.endpoints import docs

app = Flask(__name__)
app.register_blueprint(docs)


@dataclass
class HelloResponse(Response):
    message: str
    status: str

@dataclass
class HelloRequest(Request):
    message: str

@app.post("/hello")
def hello():
    r = HelloRequest.from_flask(request)
    return HelloResponse(r.message, "OK").to_dict()


if __name__ == "__main__":
    app.run(debug=True)
