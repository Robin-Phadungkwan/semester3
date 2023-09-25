#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from .db import db_connection, teardown_db, insert_user, select_user


app = Flask(__name__)
#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
register = Blueprint("register",__name__)
auth = Blueprint("auth",__name__)
userlogged = Blueprint("userlogged",__name__)
# maakt dat de wachtwoorden worden gehashed.

@property
def password(self):
    raise AttributeError('password is not a readable attribute')

@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)
#hier wordt gekeken of het wachtwoord klopt aan de hash.
def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

@auth.route('/',methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        #maakt het dat de sessie wordt behouden en dat de gebruiker wordt ingelogd.
        #hier wordt de username en het wachtwoord opgehaald.
        hashpw = check_password_hash
        username = request.form['username']
        password = request.form['password']
        #hier wordt de data in de database gestopt of gehaald
        select_user(username, password)
        return redirect(url_for('userlogged.loggedin', username = username, password = password))
    return render_template("login.html", alert = "Wrong username or password")

@register.route('/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        hashpw = generate_password_hash(request.form['password'], method= 'pbkdf2:sha256', salt_length=12)
        #hier wordt de username en het wachtwoord van de form afgenomen.
        Username = request.form['username']
        #password = request.form['password']
        #hier wordt de data in de database gestopt
        insert_user(Username, hashpw)
        return redirect (url_for('auth.login', Username = Username, password = password))
    return render_template("sign-up.html")


@about.route('/')
def over():
    return render_template("about.html")

@userlogged.route('/', methods=['GET','POST'])
def loggedin():
    if request.method == 'POST':
        secrets = request.form['secrets']
    return render_template("logged-in.html")

@bp.route("/")
def index():
    return render_template("home/index.html")

