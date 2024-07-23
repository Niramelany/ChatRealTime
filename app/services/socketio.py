from app.extensions import socketio
from flask_socketio import send,emit
from flask import request
listUsers={}

@socketio.on('message')
def handleMessage(msg):
    print(f'Message de {request.sid}: {msg}')
    emit('message-sent',{"user":listUsers.get(request.sid),'msg':msg}, room=request.sid,json=True)
    emit('message-received',{"user":listUsers.get(request.sid),'msg':msg}, broadcast= True,json=True,include_self=False)

@socketio.on('connect')
def connect():
    print(f"Nuevo cliente conectado: {request.sid}")
    
@socketio.on('user_connect')
def user_connect(user):
    listUsers[request.sid]=user
    listu=[v for k, v in listUsers.items()]
    emit('user_connect_list',{'user':listu},json=True,broadcast=True)
    emit('user_connected',{'user':listUsers.get(request.sid)},json=True,broadcast=True,include_self=False)
    
@socketio.on('disconnect')
def connect():
    print(f"cliente desconectado: {listUsers.get(request.sid,'desconocido')}")
    emit('user_disconnect',{'user':listUsers.get(request.sid,'desconocido')},json=True,broadcast=True)
    listUsers.pop(request.sid)
    listu=[v for k, v in listUsers.items()]
    emit('user_connect_list',{'user':listu},json=True,broadcast=True)