#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect,flash
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_connection, teardown_db, insert_user,select_user,insert_secret
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
def password(self, password):
    self.password_hash = generate_password_hash(password)
#hier wordt gekeken of het wachtwoord klopt aan de hash.
def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

@bp.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session.permanent = True
        select_user(username)
        session["username"] = select_user(username)
        return redirect(url_for('home.loggedin', flash = flash))
    else:
        if 'username' in session:
            return redirect(url_for('home.loggedin'))
        
        
        return render_template("login.html")

@bp.route('/register/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        error = None
        hashpw = generate_password_hash(request.form['password'], method= 'pbkdf2:sha256', salt_length=12)
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
        #Secrets = request.form['geheim']
        #print (request.form.get('sus'))
        #print(request.form.get('name'))
        #name = request.form['name']
        #insert_secret(name,Secrets, Username)
        return render_template("logged-in.html", Username=Username)
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

