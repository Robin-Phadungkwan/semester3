#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect,flash
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_connection, teardown_db, insert_user,select_user,insert_secret,select_secret,select_password
from datetime import timedelta

#hier worden de blueprints gemaakt.
app = Flask(__name__)
bp = Blueprint("home", __name__)
app.permanent_session_lifetime = timedelta(minutes=5) #hier wordt de session lifetime gemaakt.
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
            session.permanent = True #hier wordt de session permanent gemaakt.
            session["username"] = username #hier wordt de username in de session gezet.
            flash("Login successful", "success") #hier wordt een flash op het scherm gezet.
            return redirect(url_for('home.loggedin')) #hier wordt je gereturned naar de loggedin pagina.
        else:
            flash("Invalid username or password", "error") #hier wordt een flash op het scherm gezet als de login of password fout is.

    if 'username' in session:
        return redirect(url_for('home.loggedin'))

    return render_template('login.html') 
        
@bp.route('/register/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        #hier wordt de hash gemaakt van het wachtwoord.
        hashpw = generate_password_hash(request.form['password'], method= 'pbkdf2:sha256',salt_length=12)
        #hier wordt de username en het wachtwoord van de form afgenomen.
        Username = request.form['username']
        #hier wordt gekeken of de username en het wachtwoord niet te lang zijn en als hij te lang is dan moet er een flash op het scherm komen.
        if len (Username) > 256: #als de lengte van de username langer is dan 256 dan moet er een flash op het scherm komen.
            flash ('Username is too long')
        password = request.form['password'] # hetzelfde als hierboven maar dan voor het wachtwoord.
        if len (password) > 256:
            flash ('Password is too long')
        #hier wordt de data in de database gestopt.
        passed = insert_user(Username, hashpw) #hier wordt de data in de database gestopt.
        #als de data al bestaat in de database dan moet er een flash op het scherm komen waarin wordt gezegd dat de username al bestaat(db.py) en wordt je gereturned.
        if passed == None:
            return render_template("sign-up.html")
        else:   #anders mag je naar de login pagina.
            flash ('You are now registered') 
            return redirect (url_for('home.login')) 
    if 'username' in session:
        return redirect(url_for('home.loggedin')) #als de username in de session zit dan wordt je gereturned naar de loggedin pagina.   
    return render_template("sign-up.html") #hier wordt de sign-up pagina gerendered.

@bp.route('/about/')
def over():
    return render_template("about.html")

@bp.route('/logged-in/', methods=['GET','POST'])
def loggedin():
    if 'username' in session: #als de username in de session zit dan mag je naar de logged-in pagina.
        Username = session['username'] #hier wordt de username uit de session gehaald.
        if request.method == 'POST': #als de request een post is dan mag je de data in de database stoppen.
            name = request.form['name'] #hier wordt de naam uit de form gehaald.
            info = request.form['info'] # hier wordt de info uit de form gehaald.
            Username = session['username'] #hier wordt de username uit de session gehaald.
            insert_secret(name,info,Username) #hier wordt de data in de database gestopt.
            flash ('You have added a secret') #hier wordt een flash op het scherm gezet.
            return redirect (url_for('home.loggedin', flash=flash, Username=Username, insert_secret=insert_secret)) #hier wordt je gereturned naar de logged-in pagina met wat data.
        return render_template("logged-in.html",flash=flash,insert_secret=insert_secret, Username=Username) #hier wordt de logged-in pagina gerendered met username en flash en secret data.
    else: #als de username niet in de session zit dan wordt je gereturned naar de login pagina.
        return redirect(url_for('home.login'))
    
@bp.route("/logout") #hier wordt de logout functie gemaakt.
def logout(): #hier wordt de logout functie gemaakt.
    session.pop("username", None) #hier wordt de username uit de session gehaald.
    flash("You have been logged out.","info") #hier wordt een flash op het scherm gezet.
    return redirect(url_for("home.index")) #hier wordt je gereturned naar de index pagina.

@bp.route("/")
def index():
    return render_template("home/index.html")