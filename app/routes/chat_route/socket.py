from flask import Blueprint, request,jsonify
from jwt import ExpiredSignatureError, InvalidSignatureError
from app.extensions import socketio,jwt
from flask_socketio import send,emit
from flask_jwt_extended import JWTManager, verify_jwt_in_request,current_user,get_jwt_identity
from flask_jwt_extended import exceptions,get_jwt
from flask import request
import functools

socket_bp = Blueprint('socket', __name__)

@socket_bp.route('/')
def func_name(foo):
    pass

""" @jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    #print(jwt_payload)
    return jsonify(code="dave", err="I can't let you do that"), 401 """
    

listUsers={}


def jwt_required_socket(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            if 'Authorization' in request.headers:
                verify_jwt_in_request()
            else:
                token = request.args.get('token')
                if token:
                    request.headers = {'Authorization': f'Bearer {token}'}
                    verify_jwt_in_request()
                else:
                    emit('disconnect', {'message': 'NoAuthorizationHeader'}, namespace='/')
                    return False
        except ExpiredSignatureError:
            print("error: ExpiredSignatureError")
            emit('disconnect', {'message': 'jwt expired'}, namespace='/')
            return False
        except InvalidSignatureError:
            print("error: InvalidSignatureError")
            emit('disconnect', {'message': 'jwt expired'}, namespace='/')
            return False
        except Exception as e:
            print(f"Error: {e}")
            emit('disconnect', {'message': str(e)}, namespace='/')
            return False
        return f(*args, **kwargs)
    return wrapped

@socketio.on('connect')
@jwt_required_socket
def handle_connect():
    print(f"Nuevo cliente conectado:")
    emit('message', f'Mensaje recibido! {current_user.username}', broadcast=True)

@socketio.on('user_connect')
@jwt_required_socket
def user_connect(user):
    pass
    #user = get_jwt_identity()
    #print(f"Nuevo cliente conectado{user.id_user}")
    #print(f"Nuevo cliente conectado: {request.sid}")
    """ listUsers[request.sid]=user
    listu=[v for k, v in listUsers.items()]
    emit('user_connect_list',{'user':listu},json=True,broadcast=True)
    emit('user_connected',{'user':listUsers.get(request.sid)},json=True,broadcast=True,include_self=False) """


@socketio.on('message')
@jwt_required_socket
def handleMessage(msg):
    print('header',request.headers)
    print(f'Message de {request.sid}: {msg}')
    emit('mensaje', { 'contenido': 'Mensaje recibido!' })
    emit('message-sent',{"user":listUsers.get(request.sid),'msg':msg}, room=request.sid,json=True)
    emit('message-received',{"user":listUsers.get(request.sid),'msg':msg}, broadcast= True,json=True,include_self=False)
    

@socketio.on('disconnect')
@jwt_required_socket
def disconnect():
    pass
    """ print(f"cliente desconectado: {listUsers.get(request.sid,'desconocido')}")
    emit('user_disconnect',{'user':listUsers.get(request.sid,'desconocido')},json=True,broadcast=True)
    listUsers.pop(request.sid)
    listu=[v for k, v in listUsers.items()]
    emit('user_connect_list',{'user':listu},json=True,broadcast=True) """