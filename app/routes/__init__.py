def register_routes(app):
    from app.routes.chat_route.chat import chat_bp
    from app.routes.login_route.login import login_bp
    from app.routes.user_route.user import user_bp
    from app.routes.chat_route.socket import socket_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(socket_bp, url_prefix='')
    app.register_blueprint(login_bp, url_prefix='')
    app.register_blueprint(user_bp, url_prefix='/user')