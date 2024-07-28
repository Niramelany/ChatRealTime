from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "USERS"
    id_user = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_passwd(self, passwd):
        self.passwd = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.passwd, passwd)

    def save(self):
        if not self.id_user:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_user):
        return Usuario.query.get(id_user)

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(username=username).first()


class Solicitud(db.Model):
    __tablename__ = "SOLICITUDES"
    id_solicitud = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user_snd = db.Column(db.Integer, db.ForeignKey("USERS.id_user"), nullable=False)
    id_user_rcv = db.Column(db.Integer, db.ForeignKey("USERS.id_user"), nullable=False)
    status = db.Column(
        db.Enum("pendiente", "aceptada", "rechazada"),
        nullable=False,
        default="pendiente",
    )
    user_snd = db.relationship("Usuario", foreign_keys=[id_user_snd])
    user_rcv = db.relationship("Usuario", foreign_keys=[id_user_rcv])

    def send(self):
        if not self.id_solicitud:
            db.session.add(self)
        db.session.commit()
    
    def accepted(self):
        if self.id_solicitud:
            print(self.id_solicitud)
            self.status="aceptada"
        db.session.commit()
    
    def rejected(self):
        if self.id_solicitud:
            self.status="rechazada"
        db.session.commit()

    def check_status(self):
        return self.status

    @staticmethod
    def check_solicitud(user_snd, user_rcv):
        return Solicitud.query.filter_by(
            id_user_snd=user_snd, id_user_rcv=user_rcv
        ).first()
        
    @staticmethod
    def get_by_username(user_id):
        return Solicitud.query.filter_by(
            id_user_rcv=user_id
        ).join(Solicitud.user_rcv).all()
    
    @staticmethod
    def get_by_id(id_solicitud):
        return Solicitud.query.get(id_solicitud)
    
    def to_json(self):
        return{
            "id_solicitud":self.id_solicitud,
            "nombre":self.user_snd.nombre,
            "username":self.user_snd.username,
            "estado":self.status
        }
    
