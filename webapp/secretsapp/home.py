#hier wordt aangegeven wat er geimporteerd moet worden.
import functools
from flask import Flask, Blueprint,render_template, request,session,url_for,redirect
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
#hier worden de blueprints gemaakt.
bp = Blueprint("home", __name__)
about = Blueprint("about",__name__)
views = Blueprint("views",__name__)
auth = Blueprint("auth",__name__)
userlogged = Blueprint("userlogged",__name__)

cnx = mysql.connector.connect(
            host="secrets-db",
            user="secrets",
            password="BestPassword",
            database="secrets"
        )
cursor = cnx.cursor()
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'secrets'
#app.config['MYSQL_PASSWORD'] = 'BestPassword'
#app.config['MYSQL_DB'] = 'secretsapp'
#mysql = MySQL(app)*
#hier maak ik de routes aan naar de website en geef ik login en sign-up een post/get methode mee
@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        add_user = ("INSERT INTO User" "(username, password_hash)" "VALUES (%s, %s)")
        data_user = (request.form['username'], request.form['password'])
        cursor.execute(add_user, data_user)
        cnx.commit()
        cursor.close()
        cnx.close()

        #cur = mysql.connection.cursor()
        #cur.execute("INSERT INTO users(username,password_hash) VALUES(%s,%s)",(username,password))
        #mysql.connection.commit()
        #cur.close()
        return redirect(url_for('auth.login'))
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
