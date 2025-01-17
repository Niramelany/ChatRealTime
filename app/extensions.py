from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt=JWTManager()
cors=CORS()
socketio = SocketIO(cors_allowed_origins="*")