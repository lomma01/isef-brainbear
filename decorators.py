from flask import redirect
from flask import session
from flask import url_for
from functools import wraps
import sqlite3 as sql
from wtforms import Form, StringField

# put your user_id here
ADMINS = ["github|59766382", "github|37813763", "github|95571837", "github|59029239"]

# Decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated


# Helper Functions
# Checks if user_id from session is present in userstore from db and member of specific role
def is_admin():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    userstore = cur.execute("SELECT * FROM users;").fetchall()
    if session["profile"]["user_id"] in ADMINS:
        # SQL Satement: UPDATE role to is_admin
        return True
    else:
        for i in userstore:
            if session["profile"]["user_id"] in i and "is_admin" in i:
                return True
            else:
                return False


def is_dozent():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    userstore = cur.execute("SELECT * FROM users;").fetchall()
    for i in userstore:
        if session["profile"]["user_id"] in i and "is_dozent" in i:
            return True
        else:
            continue


def is_student():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    userstore = cur.execute("SELECT * FROM users;").fetchall()
    for i in userstore:
        if session["profile"]["user_id"] in i and "is_student" in i:
            return True
        else:
            continue


# Authorization decorators
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not is_admin():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


def not_admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if is_admin():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


def dozent_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not is_dozent():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


def not_dozent_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if is_dozent():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


def student_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not is_student():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


def not_student_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if is_student():
            return redirect(url_for("error"))
        return f(*args, **kwargs)

    return decorated_function


class UpdateRoles(Form):
    id = StringField('ID')
    role = StringField('Rolle')