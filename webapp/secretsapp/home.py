#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Blueprint,flash,g,redirect, render_template, request,session,url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db
import mysql.connector

#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
loggedin= Blueprint("logged-in",__name__)
def db_connection():
    con

#hier maak ik de routes aan naar de website en geef ik login en sign-up een post/get methode mee

@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?",(username,)
        ).fetchone()

        if user is None:
            error = 'incorrect Username'
        elif not check_password_hash(user['password'],password):
            error = 'incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for("logged-in"))
        flash(error)
    return render_template("login.html")

@views.route('/',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username,password) VALUES (?,?)",
                    (username,generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"user {username} is already registered"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("sign-up.html")
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@about.route('/')
def over():
    return render_template("about.html")

@loggedin.route('/')
def loggedin():
    return render_template("logged-in.html")

@bp.route("/")
def index():
    return render_template("home/index.html")
