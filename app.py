import os

from flask import Flask, render_template, request, redirect, url_for, session
from scripts.functions import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/contact')
def contact_page():
    return render_template("contact.html")


@app.route('/login', methods=["GET", "POST"])
def login_page():
    message = "none"
    try:
        if request.method == "POST":
            email = request.form.get("emailInput").strip()
            password = request.form.get("passwordInput").strip()

            if login(email, password):
                message = "Admin account"
            else:
                message = "Normal Account"
    except Exception as e:
        message = "Wrong Email or Password try again"
        print(e)
    return render_template("login.html", message=message)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    return render_template("register.html")


@app.route('/logout')
def logout_page():
    session.pop('logged_in', None)
    session.pop('bearer_code', None)
    session.pop('admin', None)
    return redirect(url_for('home_page'))


if __name__ == "__main__":
    app.run()
