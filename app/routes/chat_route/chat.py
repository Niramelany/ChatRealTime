from flask import Blueprint, request, render_template,redirect
from app.extensions import socketIO
from flask_socketio import send

chat_bp = Blueprint('chat', __name__)
listUsers=[]

@chat_bp.route('/', methods=['GET'])
def new_chat():
    currentUser = request.args.get('name')
    if not currentUser:
        return redirect('/')
    listUsers.append(currentUser)
    return render_template('chat.html',currentUser=currentUser,listUsers=listUsers)

@socketIO.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)