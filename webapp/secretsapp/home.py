#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from .db import db_connection, teardown_db, insert_user


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
    session.pop('username', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user(username, password)
        return redirect(url_for('userlogged.loggedin', username = username, password = password))
    else:
        pass
    return render_template("login.html", alert = "Wrong username or password")

@register.route('/',methods=['GET','POST'])
def signup():  
    if request.method == 'POST':
        Username = request.form['name']
        password = request.form['passwrd']
        insert_user(Username, password)
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

