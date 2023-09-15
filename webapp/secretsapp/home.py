from flask import Blueprint, render_template, request

bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)

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
