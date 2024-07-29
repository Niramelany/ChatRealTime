from app.extensions import db
from app.models.usuarios import Usuario

class Chats(db.Model):
    __tablename__ = "CHATS"
    id_chat=db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_name=db.Column(db.String(50), nullable=False)
    is_group=db.Column(db.Boolean, nullable=False, default=False)
    
    def save(self):
        if not self.id_chat:
            if '_to_' not in self.chat_name:
                self.is_group=True
            db.session.add(self)
        db.session.commit()
        self.id_chat=self.id_chat
        return self
    
    @staticmethod
    def get_by_id(id_chat):
        return Usuario.query.get(id_chat)

    @staticmethod
    def get_by_username(id_chat):
        return Chats.query.filter_by(id_chat=id_chat).first()
    
    def to_json(self):
        return{
            "id_chat":self.id_chat,
            "chat_name":self.chat_name,
            "is_group":self.is_group
        }

#_---
class ChatMiembros(db.Model):
    __tablename__ = "CHAT_MIEMBROS"
    id_chat=db.Column(db.Integer, db.ForeignKey("CHATS.id_chat"), primary_key=True)
    id_user=db.Column(db.Integer, db.ForeignKey("USERS.id_user"), primary_key=True)
    
    _id_chat = db.relationship("Chats", foreign_keys=[id_chat])
    _id_user = db.relationship("Usuario", foreign_keys=[id_user])
    
    def save(self):
        try:
            print('VALOR DEL self.id_chat',self.id_chat)
            print('VALOR DEL self.id_user',self.id_user)
            print('VALOR DEL CONDICIONAL',(self.id_chat is not None and self.id_user is not None))
            if self.id_chat and self.id_user:
                db.session.add(self)
            db.session.commit()
            self
        except:
            print("errro")
    
    @staticmethod
    def get_by_id_user(id_user):
        return ChatMiembros.query.filter_by(id_user=id_user).join(ChatMiembros._id_chat).all()
    """  Solicitud.query.filter_by(
        id_user_rcv=user_id
    ).join(Solicitud.user_rcv).all() """
        
    

    @staticmethod
    def get_by_username(id_chat):
        return Chats.query.filter_by(id_chat=id_chat).first()
    
    def to_json(self):
        if(not self._id_chat.is_group):
            _chat_name=self._id_chat.chat_name.split('_to_')
            print(_chat_name)
            chat_name= _chat_name[0] if self._id_user.username not in _chat_name[0] else _chat_name[1]
            user_send=Usuario.get_by_username(chat_name)
            print(chat_name)
            return {
                "is_group":self._id_chat.is_group,
                "nombre_chat":user_send.nombre,
                "from_username":self._id_user.username,
                "from_name":self._id_user.nombre,
                "to_username":user_send.username,
                "to_name":user_send.nombre,
                "room":self._id_chat.chat_name
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