import secrets

from flask import Flask
import secretsapp.home
import secretsapp.db as db

def create_app() -> Flask:
    app = Flask(__name__)
    from .views import views
    from .auth import auth
    app.config["SECRET_KEY"] = secrets.token_hex(64)

    app.teardown_appcontext(db.teardown_db)

    app.register_blueprint(secretsapp.home.bp)
    app.register_blueprint(views, url_prefix="/views/")
    app.register_blueprint(auth, url_prefix="/auth/" )
    return app
