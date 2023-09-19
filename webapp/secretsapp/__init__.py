import secrets
from flask import Flask
import secretsapp.home
import secretsapp.db as db

#hieronder wordt de flask app gemaakt en van .home de views, auth en about geimporteerd.
def create_app() -> Flask:
    app = Flask(__name__)
    from .home import views,auth,about,userlogged
    app.config["SECRET_KEY"] = secrets.token_hex(64)

    app.teardown_appcontext(db.teardown_db)
    #hieronder wordt de blueprint geregistreerd.
    app.register_blueprint(secretsapp.home.bp)
    app.register_blueprint(views, url_prefix="/register/")
    app.register_blueprint(auth, url_prefix="/login/")
    app.register_blueprint(about, url_prefix="/about/")
    app.register_blueprint(userlogged, url_prefix="/logged-in/")
    return app
