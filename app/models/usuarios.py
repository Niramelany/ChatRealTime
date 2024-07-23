from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class Usuario(db.Model, UserMixin):

    __tablename__ = 'USERS'

    id = db.Column("id_user",db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(128), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_passwd(self, passwd):
        self.passwd = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.passwd, passwd)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_user):
        return Usuario.query.get(id_user)

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()