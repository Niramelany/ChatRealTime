from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models.usuarios import Usuario,Solicitud
from app.extensions import jwt
from app.models.chats import Chats,ChatMiembros

user_bp = Blueprint("user", __name__)

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

@user_bp.route("/solicitud", methods=["GET"])
@jwt_required()
def get_solicitud():
    id_user=current_user.id_user
    print(f'user {current_user.nombre} solicita listado de solicitudes')
    query=Solicitud.get_by_username(id_user)
    list_solicitud=[]
    for solicitud in query:
        list_solicitud.append(solicitud.to_json())
    return jsonify(list_solicitud=list_solicitud)

@user_bp.route("/solicitud", methods=["POST"])
@jwt_required()
def add_friend():
    print(request.json)
    tipo_solicitud = request.json.get("tipo_solicitud", None)
    user_service = request.json.get("username", None)
    if tipo_solicitud is None and user_service is None:
        return jsonify(request_error="No se detecta datos"), 400
    user_aux = Usuario.get_by_username(user_service)
    if user_aux is None:
        return jsonify("El usuario ingresado no existe"), 400
    if user_aux.id_user==current_user.id_user:
        return jsonify("¿¿Intentas enviarte solicitud a ti mismo??"), 400
    ##comprobamos la solicitud
    if tipo_solicitud =='envio':
        #id_user_snd el que envia, id_user_rcv el que recibe
        solicitud=Solicitud.check_solicitud(user_snd=current_user.id_user,user_rcv=user_aux.id_user)
        if solicitud is None:
            solicitud=Solicitud(id_user_snd=current_user.id_user,id_user_rcv=user_aux.id_user)
            solicitud.send()
            return jsonify(msg_ok="solicitud enviada"),201
        else:
            return jsonify(f'Solicitud en estado {solicitud.check_status()}'),400
    elif tipo_solicitud=='acepta':
        solicitud=Solicitud.check_solicitud(user_snd=user_aux.id_user,user_rcv=current_user.id_user)
        if solicitud is not None:
            solicitud.accepted()
            if(solicitud.check_status()=='aceptada'):
                chat=Chats(chat_name=f'{user_aux}_to_{current_user.username}')
                chat.save()
                user_snd=ChatMiembros(id_chat=chat.id_chat,id_user=current_user.id_user)
                user_rcv=ChatMiembros(id_chat=chat.id_chat,id_user=user_aux.id_user)
                user_snd.save()
                user_rcv.save()
                return jsonify(msg_ok=solicitud.check_status()),201
            else:
                return jsonify(msg_ok=solicitud.check_status()),400
    elif tipo_solicitud=='rechaza':
        solicitud=Solicitud.check_solicitud(user_snd=user_aux.id_user,user_rcv=current_user.id_user)
        if solicitud is not None:
            solicitud.rejected()
            return jsonify(msg_ok=solicitud.check_status()),201
    else:
        return jsonify(f'Tipo de solicitud ingresada invalida:{tipo_solicitud}'), 400
    return jsonify("Nada que retornar"),400


@user_bp.route("/addGroup", methods=["POST"])
def add_group():
    data = request.json
    print(data["to"])
    user = Usuario.get_by_username(data["to"])
    if user is not None:
        error = "El nombre de usuario ya existe"
    return {"hola": 2}, 201
