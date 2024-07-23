from flask import Blueprint, request, render_template,redirect
from flask_login import current_user,login_required
from app.extensions import login_manager
from app.models.usuarios import Usuario

chat_bp = Blueprint('chat', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

@chat_bp.route('/')
@login_required
def new_chat():
    return render_template('chat.html')