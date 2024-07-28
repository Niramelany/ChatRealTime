from app.extensions import db
from app.models.usuarios import Usuario

class Chats(db.Model):
    __tablename__ = "CHATS"
    id_chat=db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_name=db.Column(db.String(50), nullable=False)
    is_group=db.Column(db.Boolean, default=False)
    
    def save(self):
        if not self.id_chat:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id_chat):
        return Usuario.query.get(id_chat)

    @staticmethod
    def get_by_username(id_chat):
        return Chats.query.filter_by(id_chat=id_chat).first()

#_---
class ChatMiembros(db.Model):
    __tablename__ = "CHAT_MIEMBROS"
    id_chat=db.Column(db.Integer, db.ForeignKey("CHATS.id_chat"), primary_key=True)
    id_user=db.Column(db.Integer, db.ForeignKey("USERS.id_user"), primary_key=True)
    
    _id_chat = db.relationship("Chats", foreign_keys=[id_chat])
    _id_user = db.relationship("Usuario", foreign_keys=[id_user])
    
    def save(self):
        if not self.id_chat and not self.id_user:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id_user(id_user):
        return ChatMiembros.query.filter_by().join(ChatMiembros._id_chat).all()
    """  Solicitud.query.filter_by(
        id_user_rcv=user_id
    ).join(Solicitud.user_rcv).all() """
        
    

    @staticmethod
    def get_by_username(id_chat):
        return Chats.query.filter_by(id_chat=id_chat).first()
    
    def to_json(self):
        return {
            "es_grupo":self._id_chat.is_group,
            "nombre_chat":self._id_chat.chat_name,
            "username":self._id_user.username,
            "nombre":self._id_user.username
        }
    
#----
class Mensajes(db.Model):
    __tablename__ = "MENSAJES"
    id_mensaje=db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_chat=db.Column(db.Integer, db.ForeignKey("CHATS.id_chat"))
    id_user=db.Column(db.Integer, db.ForeignKey("USERS.id_user"))
    mensaje=db.Column(db.Text)
    timestamp=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    
    _id_chat = db.relationship("Chats", foreign_keys=[id_chat])
    _id_user = db.relationship("Usuario", foreign_keys=[id_user])
    
    def save(self):
        if not self.id_mensaje:
            db.session.add(self)
        db.session.commit()