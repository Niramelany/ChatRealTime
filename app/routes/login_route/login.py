from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,jwt_required,current_user
from sqlalchemy.exc import OperationalError
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

@login_bp.route('/login', methods=['POST'])
def login_route():
    try:
        username=request.json.get("username", None)
        password=request.json.get("password",None)
        if username is None and password is None:
            return jsonify("No se detecta datos"),400
        user = Usuario.get_by_username(username)
        if user is not None and user.check_passwd(password):
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token),200
        else:
            return jsonify("Usuario y/o contraseña incorrectos"),400
    except OperationalError as error:
        sql_error=error._sql_message()
        print(error)
        if '2002' in sql_error:
            return jsonify("No se puede conectar al servidor MySQL (CONNECTION_ERROR)"),500
        if '2003' in sql_error:
            return jsonify("No se puede conectar al servidor MySQL (HOST_ERROR)"),500
        if '2005' in sql_error:
            return jsonify("Host de servidor MySQL desconocido"),500
        if '1061' in sql_error:
            return jsonify("Error Base de datos: Nombre de clave duplicado"),500
        return jsonify(sql_error),500
    except Exception as error:
        return jsonify(error.__cause__),500

@login_bp.route('/register', methods=['POST'])
def register_route():
    try:
        nombre=request.json.get("nombre",None)
        username=request.json.get("username",None)
        passwd=request.json.get("password",None)
        if nombre is None and username is None and passwd is None:
            return jsonify("No se detecta datos"),400
        user = Usuario.get_by_username(username)
        if user is not None:
                return jsonify("El nombre de usuario ya existe"),400
        user = Usuario(nombre=nombre, username=username)
        print(username,user.nombre)
        user.set_passwd(passwd)
        user.save()
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token,new_user=True),201
    except OperationalError as error:
        sql_error=error._sql_message()
        print(error)
        if '2002' in sql_error:
            return jsonify("No se puede conectar al servidor MySQL (CONNECTION_ERROR)"),500
        if '2003' in sql_error:
            return jsonify("No se puede conectar al servidor MySQL (HOST_ERROR)"),500
        if '2005' in sql_error:
            return jsonify("Host de servidor MySQL desconocido"),500
        if '1061' in sql_error:
            return jsonify("Error Base de datos: Nombre de clave duplicado"),500
        return jsonify(sql_error),500
    except Exception as error:
        return jsonify(error.__cause__),500

#prueba-no-prod
@login_bp.route('/logout')
@jwt_required()
def logout_route():
    """ logout_user() """
    return jsonify(smg=current_user.username)
