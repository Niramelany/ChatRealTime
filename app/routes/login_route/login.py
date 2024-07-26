from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,jwt_required,current_user
from app.models.usuarios import Usuario
from app.extensions import jwt
login_bp = Blueprint('login', __name__)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id_user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id_user=identity).one_or_none()


@login_bp.route('/login', methods=['GET'])
def login_route():
    username=request.json.get("username", None)
    password=request.json.get("password",None)
    if username is None and password is None:
        return jsonify(error="No se detecta datos"),401
    user = Usuario.get_by_username(username)
    if user is not None and user.check_passwd(password):
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token),200
    else:
        return jsonify(error="Usuario y/o contraseña incorrectos"),401


@login_bp.route('/register', methods=['POST'])
def register_route():
    nombre=request.json.get("nombre",None)
    username=request.json.get("username",None)
    passwd=request.json.get("password",None)
    if nombre is None and username is None and passwd is None:
        return jsonify(error="No se detecta datos"),401
    user = Usuario.get_by_username(username)
    if user is not None:
            return jsonify(error="El nombre de usuario ya existe"),401
    user = Usuario(nombre=nombre, username=username)
    user.set_passwd(passwd)
    user.save()
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token),201

#prueba-no-prod
@login_bp.route('/logout')
@jwt_required()
def logout_route():
    """ logout_user() """
    return jsonify(smg=current_user.username)
