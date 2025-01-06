from app.routers.start import start_bp
from app.routers.admin import admin_bp
from app.routers.webhook import weebhook_bp
def register_routers(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(weebhook_bp)
    app.register_blueprint(start_bp)