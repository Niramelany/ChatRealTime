from flask import Flask
from app.routes import register_routes
from app.extensions import socketio


def create_app():
    app = Flask(__name__)
    socketio.init_app(app)
    socketio.run(app)
    register_routes(app)
    return app
