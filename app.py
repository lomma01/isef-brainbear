from flask import Flask, render_template

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


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
