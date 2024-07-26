from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.models.usuarios import Usuario,Solicitud
from app.extensions import jwt

user_bp = Blueprint("user", __name__)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id_user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id_user=identity).one_or_none()


@user_bp.route("/solicitud", methods=["POST"])
@jwt_required()
def add_friend():
    tipo_solicitud = request.json.get("solicitud", None)
    user_service = request.json.get("username", None)
    if tipo_solicitud is None and user_service is None:
        return jsonify(request_error="No se detecta datos"), 401
    user_aux = Usuario.get_by_username(user_service)
    if user_aux is None:
        return jsonify(error="El usuario ingresado no existe"), 401
    ##comprobamos la solicitud
    if tipo_solicitud =='envio':
        #id_user_snd el que envia, id_user_rcv el que recibe
        solicitud=Solicitud.check_solicitud(user_snd=current_user.id_user,user_rcv=user_aux.id_user)
        if solicitud is None:
            solicitud=Solicitud(id_user_snd=current_user.id_user,id_user_rcv=user_aux.id_user)
            solicitud.send()
            return jsonify(msg_ok="solicitud enviada"),201
        else:
            return jsonify(msg=solicitud.check_status()),401
    elif tipo_solicitud=='acepta':
        solicitud=Solicitud.check_solicitud(user_snd=user_aux.id_user,user_rcv=current_user.id_user)
        if solicitud is not None:
            solicitud.accepted()
            return jsonify(msg_ok=solicitud.check_status()),201
    elif tipo_solicitud=='rechaza':
        solicitud=Solicitud.check_solicitud(user_snd=user_aux.id_user,user_rcv=current_user.id_user)
        if solicitud is not None:
            solicitud.rejected()
            return jsonify(msg_ok=solicitud.check_status()),201
    else:
        return jsonify(error=f'solicitud ingresada:{tipo_solicitud}, solo se admite "envio" o ""acepta"'), 401
    return jsonify(request_error="Nada que retornar"),401


@user_bp.route("/addGroup", methods=["POST"])
def add_group():
    data = request.json
    print(data["to"])
    user = Usuario.get_by_username(data["to"])
    if user is not None:
        error = "El nombre de usuario ya existe"
    return {"hola": 2}, 201
