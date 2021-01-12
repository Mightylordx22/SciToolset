import os

from flask import Flask, render_template, request, redirect, url_for, session
from scripts.functions import *
from scripts.admin_tools import gen_unique_code

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
            if email == "mightylordx786@gmail.com":
                message = "Admin account"
            else:
                message = "Normal Account"
            # if email != "mightylordx786@gmail.com":
            #     session['logged_in'] = True
            #     session['bearer_code'] = get_bearer_code()
            # else:
            #     session['logged_in'] = True
            #     session['bearer_code'] = get_bearer_code()
            #     session['admin'] = True
            #     return redirect(url_for('home_page'))
    except Exception as e:
        message = "Wrong Email or Password try again"
        print(e)
    return render_template("login.html", message=message)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    message = "none"
    try:
        if request.method == "POST":
            message = "none"
            reg = register_user(request.form.get("emailInput").strip(), request.form.get("passwordInput").strip(),
                                request.form.get("uCode").strip(), request.form.get("firstNameInput").strip(),
                                request.form.get("lastNameInput").strip())
            if type(reg) == str:
                return render_template("register.html", message=reg)
            else:
                return redirect(url_for(login_page))
    except Exception as e:
        print(e)
    return render_template("register.html", message=message)


@app.route('/logout')
def logout_page():
    session.pop('logged_in', None)
    session.pop('bearer_code', None)
    session.pop('admin', None)
    return redirect(url_for('home_page'))


@app.route('/test')
def test_page():
    gen_unique_code()
    return "Done"


if __name__ == "__main__":
    app.run()
