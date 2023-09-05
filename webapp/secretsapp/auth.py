from flask import Blueprint

auth = Blueprint("auth")

@auth.route('/login')
def login():
    return "login"