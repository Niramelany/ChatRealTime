from flask import Blueprint, render_template,request,redirect,session
login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def method_name():
    return redirect('/login')

@login_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method=="POST":
        session["user"]=request.form["nombre"]
        print(session["user"])
    return render_template('index.html')


@login_bp.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method=="POST":
        print(request.form["nombre"])
        print(request.form["username"])
    return render_template('index.html')