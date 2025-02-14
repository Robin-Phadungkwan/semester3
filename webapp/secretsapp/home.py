#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect,flash
from werkzeug.security import check_password_hash, generate_password_hash
from .db import insert_user,select_user,insert_secret,select_secret,select_password,delete_secret,share_secret,select_secret_id,select_secret_share,update_secret
from datetime import timedelta

#hier worden de blueprints gemaakt.
app = Flask(__name__)
bp = Blueprint("home", __name__)
app.permanent_session_lifetime = timedelta(minutes=5) #hier wordt de session lifetime gemaakt.
# maakt dat de wachtwoorden worden gehashed.

#hier wordt een property gemaakt voor een password.
@property
def password(self): 
    raise AttributeError('password is not a readable attribute')
#hier wordt een setter gemaakt voor een password.
@password.setter
def password(self, password: str):
    self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
#hier wordt gekeken of het wachtwoord klopt aan de hash.
def verify_password(self, password: str):
    return check_password_hash(self.password_hash, password)

# dit is de route naar de home pagina.
@bp.route("/")
def index():
    if 'username' in session:
        return render_template("home/index.html", username=session['username']) 
    return render_template("home/index.html") 

# dit is de route naar de about pagina.
@bp.route('/about/')
def over():
    if 'username' in session:
         return render_template("about.html", username=session['username'])
    return render_template("about.html") 

@bp.route('/register_help/')
def register_help():
    return render_template("help_register.html")
@bp.route('/security/')
def security():
    return render_template("security.html")
@bp.route('/security_procedures/')
def security_procedures():
    return render_template("security_procedures.html")
# hier wordt de route naar de login pagina gemaakt en als het de methode post is dan moet hij het wachtwoord en username vergelijken met die van de database.
# omdat het wachtwoord is gehashed moet je de check_password_hash gebruiken om te kijken of het wachtwoord klopt aan de hash.
# als dat zo is dan moet de gebruiker naar de loggedin pagina met de session data.
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
            flash("Login successful", "success")
            return redirect(url_for('home.loggedin'))
        else:
            flash("Invalid username or password", "error") #hier wordt een flash op het scherm gezet als de login of password fout is.
    #als de username al in de session zit dan wordt je gereturned naar de loggedin pagina.
    if 'username' in session:
        return redirect(url_for('home.loggedin'))
    return render_template('login.html') 

# hier wordt de data dat is ingevoerd in de database gestopt en het wachtwoord word voordat hij in de database wordt gestopt eerst gehashed.
# als de user al een session heeft dan wordt hij gereturned naar de loggedin pagina.        
@bp.route('/register/',methods=['GET','POST'])
def signup(): 
    #post request om de data aan te maken
    if request.method == 'POST':
        #hier wordt de hash gemaakt van het wachtwoord.
        hashpw = generate_password_hash(request.form['password'], method= 'pbkdf2:sha256',salt_length=12)
        #hier wordt de username en het wachtwoord van de form afgenomen.
        username = request.form['username']
        #hier wordt gekeken of de username en het wachtwoord niet te lang zijn en als hij te lang is dan moet er een flash op het scherm komen.
        if len (username) > 30: #als de lengte van de username langer is dan 256 dan moet er een flash op het scherm komen.
            flash ('Username is too long')
        password = request.form['password'] # hetzelfde als hierboven maar dan voor het wachtwoord.
        if len (password) > 255:
            flash ('Password is too long')
        #hier wordt de data in de database gestopt.
        passed = insert_user(username, hashpw) #hier wordt de data in de database gestopt.
        #als de data al bestaat in de database dan moet er een flash op het scherm komen waarin wordt gezegd dat de username al bestaat(db.py) en wordt je gereturned.
        if passed == None:
            return render_template("sign-up.html")
        else:   #anders mag je naar de login pagina.
            flash ('You are now registered') 
            return redirect (url_for('home.login')) 
    if 'username' in session:
        return redirect(url_for('home.loggedin'))
    return render_template("sign-up.html") 


# als de username in de session zit dan mag je naar de logged-in pagina, als dat niet zo is dan wordt de gebruiker terugestuurd naar de login pagina.
# als de request een post is dan mag je de data in de database stoppen, maar als je naam voor het ding te lang is of de info is te lang dan gaat het niet in de database.
@bp.route('/logged-in/', methods=['GET','POST'])
def loggedin():
    if 'username' in session: 
        username = session['username']
        secrets = select_secret(username) 
        shared_secrets = select_secret_share(username)
        if request.method == 'POST': 
            name = request.form['name'] 
            info = request.form['info'] 
            username = session['username'] 
            if len(name)> 30:
                flash("your name for it is too long")
            if len(info)> 255:
                flash("your secret is too long")
            insert_data = insert_secret(name,info,username) 
            flash ('You have added a secret') 
            return redirect (url_for('home.loggedin', flash=flash, username=username, insert_data=insert_data, secrets=secrets,shared_secrets=shared_secrets))
        return render_template("logged-in.html",flash=flash,secrets=secrets,shared_secrets=shared_secrets, username=username)
    else: 
        return redirect(url_for('home.login'))
    
# hiermee kan je je geheimen delen met een andere gebruiker die in de database zit.  
@bp.route("/share/<int:id>", methods=["GET", "POST"])
def share(id): 
    if 'username' in session :
        secrets = select_secret_id(id)
        if request.method == "POST": 
            username = request.form["username"] 
            if select_user(username) == None: 
                flash("Username does not exist", "error")  
                return redirect(url_for("home.loggedin")) 
            try:
                shared_data = share_secret(id,username) 
                flash("You have shared a secret")  
                return redirect(url_for("home.loggedin", flash=flash,shared_data=shared_data)) 
            except:
                flash("You have already shared this secret with this user", "error")
        return render_template("share.html",secrets=secrets,username=session['username'])
    
    else: 
        return redirect(url_for("home.login")) 

# hier worden de route aangemaakt voor om de geheimen te updaten.
# hiervoor is een functie aangemaakt in db.py die de data opdate op basis van de id van het geheim.
# daarna wordt het met met update_secret in de database gestopt op de plek van de oude data op basis van het id.
# daarna wordt je terugegstuurd naar de loggedin pagina met een bericht waar in staat dat je een geheim hebt geupdate.    
@bp.route("/update/<int:id>", methods=["GET", "POST"]) #hier wordt de update functie gemaakt.
def update(id): 
    if 'username' in session: 
        secrets = select_secret_id(id)
        if request.method == "POST": 
            name = request.form["name"] 
            info = request.form["info"] 
            update_data = update_secret(name,info,id) 
            flash("You have updated a secret")  
            return redirect(url_for("home.loggedin", flash=flash,update_data=update_data)) 
        return render_template("update.html",secrets=secrets,Username=session['username']) 
    else: 
        return redirect(url_for("home.login"))


#hier wordt de logout functie gemaakt en wordt de gebruiker "uitgelogd" en wordt de sessie afgesloten.
@bp.route("/logout") 
def logout(): 
    session.pop("username", None)
    flash("You have been logged out.","info")  
    return redirect(url_for("home.index")) 

#hier wordt de delete functie gemaakt en wordt de data uit de database verwijdert op basis van het id.
@bp.route("/delete/<int:id>") 
def delete(id):
    delete_secret(id) 
    flash("You have deleted a secret")  
    return redirect(url_for("home.loggedin", flash=flash)) 

