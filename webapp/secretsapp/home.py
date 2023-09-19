#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash

#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
userlogged = Blueprint("userlogged",__name__)


#hier maak ik de routes aan naar de website en geef ik login en sign-up een post/get methode mee

@auth.route('/',methods=['GET','POST'])
def login():
    return render_template("login.html")

@views.route('/',methods=['GET','POST'])
def signup():  
    return render_template("sign-up.html")


@about.route('/')
def over():
    return render_template("about.html")

@userlogged.route('/')
def loggedin():
    return render_template("logged-in.html")

@bp.route("/")
def index():
    return render_template("home/index.html")
