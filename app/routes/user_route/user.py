from flask import Blueprint, request,sessions
user_bp = Blueprint('user', __name__)

@user_bp.route('/addAmigo',methods=['POST'])
def add_amigo():
    
    pass
