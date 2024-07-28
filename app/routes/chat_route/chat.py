from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.extensions import jwt
from app.models.usuarios import Usuario
from app.models.chats import Chats,ChatMiembros

chat_bp = Blueprint('chat', __name__)
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id_user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id_user=identity).one_or_none()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    #print(jwt_payload)
    return jsonify(code="dave", err="I can't let you do that"), 401


@chat_bp.route('/list')
@jwt_required()
def new_chat():
    list_chats=ChatMiembros.get_by_id_user(current_user.id_user)
    _list_chats=[]
    for chat in list_chats:
        _list_chats.append(chat.to_json())
    print(ChatMiembros.get_by_id_user(current_user.id_user))
    return jsonify(list_chats=_list_chats),200