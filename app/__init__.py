from flask import Flask
from app.routes import register_routes
from app.extensions import socketio,migrate,cors,jwt,db,ma
from app.config import Config
from dotenv import load_dotenv
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    cors.init_app(app)
    socketio.init_app(app,cors_allowed_origins="*")
    socketio.run(app,debug=False)
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    register_routes(app)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    return app
