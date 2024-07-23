from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

socketio = SocketIO()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()