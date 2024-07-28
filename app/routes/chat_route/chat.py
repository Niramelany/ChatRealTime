from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def new_chat():
    print('')
    