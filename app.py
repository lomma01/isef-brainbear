from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = "T5BPYMJD9GVKURSGTAXC"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy(app)


class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(50))


def __init__(self, username, email):
   self.username = username
   self.email = email


# Routes
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/single')
def single():
    return render_template('single.html')


@app.route('/multi')
def multi():
    return render_template('multi.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/rank')
def rank():
    return render_template('rank.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html', students=students.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['email']:
            flash('Please enter all the fields', 'error')
        else:
         student = students(username = request.form['username'], email = request.form['email'])
         
         db.session.add(student)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('signup'))
    return render_template('new.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
