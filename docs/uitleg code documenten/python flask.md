# python flask 
hieronder de code die is gemaakt, hieraan importeer ik secrets,flask van flask, secretsapp.home en importeer ik secretsapp als db.
verder maak ik de flask app aan en geef ik aan dat hij views,auth en about uit .home (home.py) moet importeren zodat hij later kan worden gebruikt.

```python

import secrets
from flask import Flask
import secretsapp.home
import secretsapp.db as db

#hieronder wordt de flask app gemaakt en van .home de views, auth en about geimporteerd.
def create_app() -> Flask:
    app = Flask(__name__)
    from .home import views,auth,about
    app.config["SECRET_KEY"] = secrets.token_hex(64)

```

hieronder wordt een functie geregistreerd wanneer de aplicatie context endigt.

```python
    app.teardown_appcontext(db.teardown_db)
```
hieronder worden de blueprints geregistreerd en wordt er aan flask verteld welke blueprint naar welke url prefix moet gaan.

```python
    #hieronder wordt de blueprint geregistreerd.
    app.register_blueprint(secretsapp.home.bp)
    app.register_blueprint(views, url_prefix="/sign-up/")
    app.register_blueprint(auth, url_prefix="/login/" )
    app.register_blueprint(about, url_prefix="/about/")
    return app

```

maar voordat dit allemaal werkt moet flask wel weten waar hij naartoe moet. dat regel je in home.py, daar ga ik hieronder op in.

# home.py

ik heb hier aangegeven dat van flask de blueprint,render template en request moet worden geimporteerd daarna worden de blueprint gemaakt en wordt er aangegeven dat flask erbij hoort(```__name__```)
de namen zijn voor elke website of html die je hebt gemaakt
hieronder de code:

``` python
#hier wordt aangegeven wat er geimporteerd moet worden.
from flask import Blueprint, render_template, request
#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
```
ik heb hier de routes aangemaakt waardoor flask weet welke link welk html bestand nodig heeft, bij de login en sign up is er ook een GET/POST methode toegevoegd zodat de input van de gebruiker bij die websites in de database wordt gestopt
```python
#hier maak ik de routes aan naar de website en geef ik login en sign-up een post/get methode mee
@auth.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template("login.html")
@views.route('/register/',methods=['GET','POST'])
def signup():
    return render_template("sign-up.html")
@about.route('/')
def over():
    return render_template("about.html")
@bp.route("/")
def index():
    return render_template("home/index.html")
```