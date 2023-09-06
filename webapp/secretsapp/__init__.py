import secrets

from flask import Flask
import secretsapp.home
import secretsapp.db as db

def create_app() -> Flask:
    app = Flask(__name__)
    from .views import views
    from .auth import auth
    from .about import about
    app.config["SECRET_KEY"] = secrets.token_hex(64)

    app.teardown_appcontext(db.teardown_db)

    app.register_blueprint(secretsapp.home.bp)
    app.register_blueprint(views, url_prefix="/sign-up/")
    app.register_blueprint(auth, url_prefix="/login/" )
    app.register_blueprint(about, url_prefix="/about/")
    return app
