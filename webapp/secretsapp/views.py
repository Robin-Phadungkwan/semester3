from flask import Blueprint

views = Blueprint("views")

@views.route('/sign-up')
def signup():
    return "sign up"
