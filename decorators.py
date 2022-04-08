from flask import redirect
from flask import session
from flask import url_for
from functools import wraps
from wtforms import Form, StringField, SelectField, TextAreaField, validators
import database

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
    userstore = database.DatabaseManager().fetch_all_user_rows()
    if session["profile"]["user_id"] in ADMINS:
        # SQL Satement: UPDATE role to is_admin
        return True
    else:
        for i in userstore:
            if session["profile"]["user_id"] in i and "is_admin" in i:
                return True
            else:
                continue


def is_dozent():
    userstore = database.DatabaseManager().fetch_all_user_rows()
    for i in userstore:
        if session["profile"]["user_id"] in i and "is_dozent" in i:
            return True
        else:
            continue


def is_student():
    userstore = database.DatabaseManager().fetch_all_user_rows()
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
    roles = ['is_student', 'is_dozent', 'is_admin']
    userstore = database.DatabaseManager().fetch_all_user_rows()
    userlist = []
    for i in userstore:
        userlist.append(i["id"])
    id = SelectField('ID', choices=userlist)
    role = SelectField('Rolle', choices=roles)


class AddModule(Form):
    course = StringField("course", validators=[validators.DataRequired()])  # Studiengang
    id = StringField('id', validators=[validators.DataRequired()])  # Kurskürzel
    designation = StringField('designation', validators=[validators.DataRequired()])  # Beschreibung des Kurses
    chapter = StringField('chapter', validators=[validators.DataRequired()])  # Kapitel / Lektion

class AddQuestions(Form):
    # modulestore = database.DatabaseManager()....
    courselist = ["Informatik", "Wirtschaftsinformatik"]  # Liste der Studiengänge
    idlist = ["IMT01", "IMT02"]  # Liste der Kurskürzel
    chapterlist = ["Lektion 1", "Lektion 2"]  # Liste der Kapitel / Lektionen
    '''for i in modulestore:
        courselist.append(i["course"])
        idlist.append(i["id"])
        chapterlist.append(i["chapter"])'''
    course = SelectField("course", choices=courselist)
    id = SelectField('id', choices=idlist)
    chapter = SelectField('chapter', choices=chapterlist)
    question = TextAreaField('question', validators=[validators.DataRequired()])
    # question = StringField('question', validators=[validators.DataRequired()])  # Frage
    answer_one = TextAreaField('answer_one', validators=[validators.DataRequired()])  # Antwort 1
    answer_two = TextAreaField('answer_two', validators=[validators.DataRequired()])  # Antwort 2
    answer_three = TextAreaField('answer_three', validators=[validators.DataRequired()])  # Antwort 3
    answer_four = TextAreaField('answer_four', validators=[validators.DataRequired()])  # Antwort 4
    hint = TextAreaField('hint')  # Hinweis optional

def output(x):
    with open("output.txt", "w") as file:
        file.write(str(x))
        file.close()