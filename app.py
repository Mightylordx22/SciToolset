from flask import Flask, render_template, request, redirect, url_for, session

import os

from scripts.functions import get_auth_data, login, register_user, get_auth_token
from scripts.admin_tools import gen_unique_code
from scripts.sci_discover import get_discover_bearer_token

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route('/')
def home_page():
    try:
        if session["auth_token"]:
            valid, new_token = get_auth_data(session["auth_token"])
            if valid:
                if new_token == -1:
                    get_discover_bearer_token()
                    return render_template("index.html")
                else:
                    session.pop('auth_token', None)
    except Exception as e:
        pass
    return redirect(url_for("login_page"))


@app.route('/contact')
def contact_page():
    return render_template("contact.html")


@app.route('/login', methods=["GET", "POST"])
def login_page():
    message = "none"
    try:
        try:
            if session["auth_token"]:
                valid, new_token = get_auth_data(session["auth_token"])
                if valid:
                    if new_token == -1:
                        return redirect(url_for("home_page"))
                    else:
                        session.pop('auth_token', None)
        except Exception as e:
            pass
        if request.method == "POST":
            email = request.form.get("emailInput").strip()
            password = request.form.get("passwordInput").strip()
            is_logged_in, status, u_id = login(email, password)
            if is_logged_in:
                # session["sci_token"], session["sci_expires"] =
                session["auth_token"] = get_auth_token(app.config.get("SECRET_KEY"), u_id)
                return redirect(url_for("home_page"))
            message = status
    except Exception as e:
        message = "Problem signing in. Please contact a admin."
        print(e)
    return render_template("login.html", message=message)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    message = "none"
    try:
        if request.method == "POST":
            reg = register_user(request.form.get("emailInput").strip(), request.form.get("passwordInput").strip(),
                                request.form.get("uCode").strip(), request.form.get("firstNameInput").strip(),
                                request.form.get("lastNameInput").strip())
            if type(reg) == str:
                return render_template("register.html", message=reg)
            else:
                return redirect(url_for("login_page"))
    except Exception as e:
        print(e)
    return render_template("register.html", message=message)


@app.route('/logout')
def logout_page():
    session.pop('auth_token', None)
    session.pop('sci_token', None)
    session.pop('sci_expires', None)
    return redirect(url_for('login_page'))


@app.route('/test')
def test_page():
    gen_unique_code()
    return "Done"


if __name__ == "__main__":
    app.run()
