from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from flask_wtf.csrf import CSRFProtect
from urllib.parse import urlencode  # Abweichung von OAuth-Quickstarts
import auth
import json
import sqlite3 as sql
import decorators
from flask import request

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

# Secret key
app.config['SECRET_KEY'] = "T5BPYMJD9GVKURSGTAXC"

# Auth0 Provider
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=auth.client_id,
    client_secret=auth.client_secret,
    api_base_url=auth.api_base_url,
    access_token_url=auth.access_token_url,
    authorize_url=auth.authorize_url,
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET'])
@decorators.requires_auth
def home():
    return render_template('home.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/single', methods=['GET'])
@decorators.requires_auth
@decorators.student_only
def single():
    return render_template('single.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/multi', methods=['GET'])
@decorators.requires_auth
@decorators.student_only
def multi():
    return render_template('multi.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/dashboard', methods=['GET'])
@decorators.requires_auth
def dashboard():
    admin = decorators.is_admin()
    dozent = decorators.is_dozent()
    student = decorators.is_student()
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4),
                           admin=admin,
                           dozent=dozent,
                           student=student)


@app.route('/rank', methods=['GET'])
@decorators.requires_auth
def rank():
    return render_template('rank.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/list', methods=['GET', 'POST'])
@decorators.requires_auth
@decorators.admin_only
def list():
    # link sql database
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    # create a cursor
    cur = con.cursor()
    cur.execute("select * from users")

    # rows to show data on /list page
    rows = cur.fetchall()

    # UPDATE roles
    roleupdate = decorators.UpdateRoles(request.form)
    if request.method == 'POST' and roleupdate.validate():
        id = roleupdate.id.data
        role = roleupdate.role.data
        # SQL Statement UPDATE roles
    
    return render_template("list.html",
                           rows=rows,
                           roleupdate=roleupdate,
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/about', methods=['GET'])
@decorators.requires_auth
def about():
    return render_template('about.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],
                                                      indent=4))


@app.route('/about2', methods=['GET'])
def about2():
    return render_template('about.html')


@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')


@app.route('/callback', methods=['GET'])
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    # column names for sql database -> you also have to change it in the database.py!!!
    username = userinfo['name']
    user_id = userinfo['sub']
    # for inital entries we use is_student
    role = 'is_student'

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (id,username,role) VALUES (?,?,?)",
            (user_id, username, role))
        con.commit()

        return redirect('/dashboard')


@app.route('/login', methods=['GET'])
def login():
    return auth0.authorize_redirect(redirect_uri=auth.redirect_uri)


@app.route('/logout', methods=['GET'])
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('index', _external=True),
        'client_id': auth.client_id
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
