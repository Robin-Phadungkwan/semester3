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

def insert_user(username, password):
    db = db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO User (username, password_hash) VALUES (%s, %s)"
    val = (username, password)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    print ("Record inserted successfully into users table")
    cursor.close()
    db.commit()

def select_user(username, password):
    db = db_connection()
    cursor = db.cursor()
    sql = "SELECT * FROM User WHERE username = %s AND password_hash = %s"
    val = (username, password)
    result = cursor.execute(sql, val)
    db.commit()
    print(result)
    print ("Record selected successfully from users table")
    cursor.close()
    db.commit()