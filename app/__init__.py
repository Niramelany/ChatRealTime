from flask import Flask
from app.routes import register_routes
from app.extensions import init_socket


def create_app():
    app = Flask(__name__)
    init_socket(app)
    register_routes(app)
    return app
