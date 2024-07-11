from flask_socketio import SocketIO

socketIO= None

def init_socket(app):
    global socketIO
    socketIO=SocketIO(app)