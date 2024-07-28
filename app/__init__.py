from flask import Flask
from app.routes import register_routes
from app.extensions import socketio,migrate,cors,jwt,db,ma
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cors.init_app(app)
    socketio.init_app(app,cors_allowed_origins="*")
    socketio.run(app,debug=True)
    db.init_app(app)
    migrate.init_app(app,db)
    ma.init_app(app)
    jwt.init_app(app)
    register_routes(app)
    return app
