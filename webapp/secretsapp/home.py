#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
userlogged = Blueprint("userlogged",__name__)


@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('userlogged.loggedin', username = username, password = password))
    else:
        pass
    return render_template("login.html")

@views.route('/',methods=['GET','POST'])
def signup():  
    return render_template("sign-up.html")


@about.route('/')
def over():
    return render_template("about.html")

@userlogged.route('/', methods=['GET','POST'])
def loggedin():
    if request.method == 'POST':
        secrets = request.form['secrets']
        redirect
    return render_template("logged-in.html")

@bp.route("/")
def index():
    return render_template("home/index.html")
