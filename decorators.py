from flask import redirect
from flask import session
from flask import url_for
from functools import wraps
from wtforms import Form, StringField, SelectField, TextAreaField, validators, BooleanField, RadioField
import database
import random

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
    for i in userstore:
        if session["profile"]["user_id"] in ADMINS or (
                session["profile"]["user_id"] in i and "is_admin" in i):
            database.update_user_role("is_admin",
                                      session["profile"]["user_id"])
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
    id = SelectField()
    role = SelectField('Rolle', choices=roles)

    def __init__(self, *args, **kwargs):
        super(UpdateRoles, self).__init__(*args, **kwargs)
        userlist = []
        for i in database.DatabaseManager().fetch_all_user_rows():
            userlist.append(i["id"])
        self.id.choices = userlist


class AddModule(Form):
    module_name = StringField('module_name',
                              validators=[validators.DataRequired()])


class EditModule(Form):
    module_name_old = SelectField()
    module_name_new = StringField("module_name_new",
                                  validators=[validators.DataRequired()])
    checkbox = BooleanField()

    def __init__(self, *args, **kwargs):
        super(EditModule, self).__init__(*args, **kwargs)
        modulelist = []
        for i in database.DatabaseManager().fetch_all_module_rows():
            modulelist.append(i["module_name"])
        self.module_name_old.choices = modulelist


class AddQuestions(Form):
    module_name = SelectField()
    chapter = StringField('chapter', validators=[validators.DataRequired()])
    question = TextAreaField('question',
                             validators=[validators.DataRequired()])
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

    def __init__(self, *args, **kwargs):
        super(AddQuestions, self).__init__(*args, **kwargs)
        modulelist = []
        for i in database.DatabaseManager().fetch_all_module_rows():
            modulelist.append(i["module_name"])
        self.module_name.choices = modulelist


class EditQuestions(Form):
    question_list = SelectField()
    fields = [
        'id', 'module_name', 'chapter', 'question', 'correct_answer',
        'wrong_answer_1', 'wrong_answer_2', 'wrong_answer_3'
    ]
    question_field_old = SelectField("question_field_old", choices=fields)
    question_field_new = StringField("question_field_new",
                                     validators=[validators.DataRequired()])
    checkbox = BooleanField()

    def __init__(self, *args, **kwargs):
        super(EditQuestions, self).__init__(*args, **kwargs)
        questions = database.lomma()
        self.question_list.choices = questions


class SolveQuestions(Form):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    con = database.DatabaseManager().conn
    cur = con.cursor()
    con.row_factory = dict_factory
    cur.execute("select * from questions")
    tupel = cur.fetchall()
    liste = []
    for i in tupel:
        liste.append(i)  # Quiz in Form einer Liste

    liste = random.sample(liste, len(liste))
    liste = liste[0]  # nur 1 Frage aus einem zufälligen Pool wählen
    answers = liste[4], liste[5], liste[6], liste[7]
    radio = RadioField("Label", choices=answers)

    def __init__(self, *args, **kwargs):
        super(SolveQuestions, self).__init__(*args, **kwargs)


def output(x):
    with open("output.txt", "w") as file:
        file.write(str(x))
        file.close()
