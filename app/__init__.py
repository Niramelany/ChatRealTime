from flask import Flask
from app.routes import register_routes
from app.extensions import login_manager,socketio,migrate,db,ma
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    socketio.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    socketio.run(app)
    register_routes(app)
    return app
