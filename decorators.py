from flask import redirect
from flask import session
from flask import url_for
from functools import wraps
from wtforms import Form, StringField, SelectField, TextAreaField, validators
import database

# put your user_id here
ADMINS = [
    "github|59766382", "github|37813763", "github|95571837", "github|59029239"
]


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
        database.update_user_role("is_admin", session["profile"]["user_id"])
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
    id = StringField('id', validators=[validators.DataRequired()])
    studiengang_name = StringField("studiengang_name",
                                   validators=[validators.DataRequired()])
    module_name = StringField('module_name',
                              validators=[validators.DataRequired()])
    designation = StringField('designation',
                              validators=[validators.DataRequired()
                                          ])  # Beschreibung des Kurses
    chapter = StringField('chapter', validators=[validators.DataRequired()
                                                 ])  # Kapitel / Lektion


class AddQuestions(Form):
    # modulestore = database.DatabaseManager()....
    courselist = ["Inf", "BWL"]  # Liste der Studiengänge
    modulelist = ["T1", "T2"]  # Liste der Kurskürzel
    chapterlist = ["L1", "L2"]  # Liste der Kapitel / Lektionen
    '''for i in modulestore:
        courselist.append(i["course"])
        idlist.append(i["id"])
        chapterlist.append(i["chapter"])'''
    studiengang_name = SelectField("studiengang_name", choices=courselist)
    module_name = SelectField('module_name', choices=modulelist)
    chapter = SelectField('chapter', choices=chapterlist)
    question = TextAreaField('question',
                             validators=[validators.DataRequired()])
    # question = StringField('question', validators=[validators.DataRequired()])  # Frage
    correct_answer = TextAreaField('correct_answer',
                                   validators=[validators.DataRequired()
                                               ])  # Antwort 1
    wrong_answer_1 = TextAreaField('wrong_answer_1',
                                   validators=[validators.DataRequired()
                                               ])  # Antwort 2
    wrong_answer_2 = TextAreaField('wrong_answer_2',
                                   validators=[validators.DataRequired()
                                               ])  # Antwort 3
    wrong_answer_3 = TextAreaField('wrong_answer_3',
                                   validators=[validators.DataRequired()
                                               ])  # Antwort 4
    hint = TextAreaField('hint')  # Hinweis optional


def output(x):
    with open("output.txt", "w") as file:
        file.write(str(x))
        file.close()