from flask import Blueprint, render_template
login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def login_route():
    return render_template('index.html')