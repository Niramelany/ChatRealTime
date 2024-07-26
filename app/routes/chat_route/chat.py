from flask import Blueprint, request, render_template,redirect
from app.models.usuarios import Usuario

chat_bp = Blueprint('chat', __name__)



@chat_bp.route('/')
def new_chat():
    return render_template('chat.html')