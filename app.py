from flask import Flask, render_template
from functions import *

app = Flask(__name__)

@app.route('/')
def index():
    if is_logged_in(0):
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()