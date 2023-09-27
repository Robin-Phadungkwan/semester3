from flask import g as app_context_global
import mysql.connector


def db_connection():
    """This function can be called to access the database connection while handling a request"""
    if 'db' not in app_context_global:
        # TODO: store config in config file
        # TODO: do not store secrets on git

        app_context_global.db = mysql.connector.connect(
            host="secrets-db",
            user="secrets",
            password="BestPassword",
            database="secrets"
        )
    return app_context_global.db


def teardown_db(exception):
    db = app_context_global.pop('db', None)

    if db is not None:
        db.close()

def insert_user(username, hashpw):
    db = db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO User (username, password_hash) VALUES (%s, %s)"
    val = (username, hashpw)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    print ("Record inserted successfully into users table")
    cursor.close()
    db.commit()

def select_user(username):
    db = db_connection()  # Assuming this function returns a database connection
    cursor = db.cursor()
    sql = "SELECT username FROM User WHERE username = %s"
    val = ( username,)  # Use a tuple with a single element
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    return result




def insert_secret(name,secrets, username):
    db = db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO Secret (name,info,user_name) VALUES (%s, %s, %s)"
    val = (name,secrets,username)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    print ("Record inserted successfully into secrets table")
    cursor.close()
    db.commit()