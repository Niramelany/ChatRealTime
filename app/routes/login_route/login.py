from flask import Blueprint, render_template,request,redirect
from flask_login import current_user,login_user
from app.extensions import login_manager
from app.models.usuarios import Usuario
login_bp = Blueprint('login', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

@login_bp.route('/')
def method_name():
    return redirect('/login')

@login_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect('/chat')
    if request.method=="POST":
        user = Usuario.get_by_username(request.form["username"])
        if user is not None and user.check_passwd(request.form["password"]):
            login_user(user)
            return redirect('/chat')
    return render_template('index.html')


@login_bp.route('/register', methods=['GET', 'POST'])
def register_route():
    if current_user.is_authenticated:
        return redirect('/chat')
    error=None
    if request.method=="POST":
        nombre=request.form["nombre"]
        username=request.form["username"]
        passwd=request.form["password"]
        user = Usuario.get_by_username(username)
        if user is not None:
            error ="El nombre de usuario ya existe"
        else:
            user = Usuario(nombre=nombre, username=username)
            user.set_passwd(passwd)
            user.save()
            login_user(user)
            return redirect('/chat')
    return render_template('register.html',error=error) 