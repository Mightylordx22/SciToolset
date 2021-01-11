from flask import Flask, render_template
from functions import foo

app = Flask(__name__)

@app.route('/')
def index():
    foo()
    return render_template("index.html")

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()