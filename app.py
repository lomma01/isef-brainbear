from flask import Flask, render_template

app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = "T5BPYMJD9GVKURSGTAXC"


# Routes
@app.route('/')
def index():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
