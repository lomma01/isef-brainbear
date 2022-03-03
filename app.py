from flask import Flask, render_template, flash, request, redirect, url_for
import sqlite3 as sql


app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = "T5BPYMJD9GVKURSGTAXC"


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
    return render_template('signup.html')


@app.route('/addrec', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            unm = request.form['username']
            email = request.form['email']
         
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students (username,email) VALUES (?,?)",(unm,email) )
            
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("added.html",msg = msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from students")
    
    rows = cur.fetchall()
    return render_template("list.html", rows = rows)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
