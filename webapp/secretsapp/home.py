#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect,flash
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_connection, teardown_db, insert_user,select_user,insert_secret,select_secret,select_password
from datetime import timedelta

#hier worden de blueprints gemaakt.
app = Flask(__name__)
bp = Blueprint("home", __name__)
app.permanent_session_lifetime = timedelta(minutes=5)
# maakt dat de wachtwoorden worden gehashed.

@property
def password(self):
    raise AttributeError('password is not a readable attribute')

@password.setter
def password(self, password: str):
    self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
#hier wordt gekeken of het wachtwoord klopt aan de hash.
def verify_password(self, password: str):
    return check_password_hash(self.password_hash, password)

@bp.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = select_user(username)
        hashed = select_password(username)
        #hier wordt gekeken of de username en het wachtwoord kloppen aan die in de database, zoja dan moet er hij naar de loggedin pagina.
        #de check_password_hash is een functie die kijkt of het wachtwoord klopt aan de hash en kies de eerste die hij ziet.
        if user and check_password_hash(hashed[0], password):
            session.permanent = True
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for('home.loggedin'))
        else:
            flash("Invalid username or password", "error")

    if 'username' in session:
        return redirect(url_for('home.loggedin'))

    return render_template('login.html') 
        

@bp.route('/register/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        error = None
        hashpw = generate_password_hash(request.form['password'], method= 'sha256')
        #hier wordt de username en het wachtwoord van de form afgenomen.
        Username = request.form['username']
        password = request.form['password'] 
        #hier wordt de data in de database gestopt
        insert_user(Username, hashpw)
        flash ('You are now registered')
        return redirect (url_for('home.login'))
    return render_template("sign-up.html")


@bp.route('/about/')
def over():
    return render_template("about.html")

@bp.route('/logged-in/', methods=['GET','POST'])
def loggedin():
    if 'username' in session:
        Username = session['username']
        if request.method == 'POST':
            name = request.form['name']
            info = request.form['info']
            Username = session['username']
            insert_secret(name,info,Username)
            flash ('You have added a secret')
            return redirect (url_for('home.loggedin', flash=flash, Username=Username, insert_secret=insert_secret))
        return render_template("logged-in.html",flash=flash,insert_secret=insert_secret, Username=Username)
    else:
        return redirect(url_for('home.login'))
    
@bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.","info")
    return redirect(url_for("home.index"))

@bp.route("/")
def index():
    return render_template("home/index.html")

