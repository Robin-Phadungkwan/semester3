#hier wordt aangegeven wat er geimporteerd moet worden.
from flask import Flask, Blueprint, render_template, request, redirect
import secrets
#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
#hier maak ik de routes aan naar de website en geef ik login en sign-up een post/get methode mee
@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template("login.html")
@views.route('/',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        pass
    return render_template("sign-up.html")

@about.route('/')
def over():
    return render_template("about.html")

@bp.route("/")
def index():
    return render_template("home/index.html")
