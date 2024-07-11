from flask import Blueprint


def register_routes(app):
    from app.routes.chat_route.chat import chat_bp
    from app.routes.login_route.login import login_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(login_bp, url_prefix='')