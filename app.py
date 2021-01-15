import os
from flask import Flask, render_template, request, redirect, url_for, session
import urllib3
urllib3.disable_warnings()
from scripts.functions import get_authenticate_data, login, get_authenticate_token, get_user_id_from_token, register, \
    authenticate_discover_bearer_token, get_user, genarate_unique_code, get_unique_codes

from scripts.josh.map_updater import get_mission_coverage

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)


@app.route('/')
def redirect_homepage():
    return redirect(url_for("home_page"))


@app.route('/map')
def home_page():
    try:
        if session["auth_token"]:
            valid, new_token = get_authenticate_data(session["auth_token"])
            if valid:
                if new_token >= 1:
                    authenticate_discover_bearer_token()
                    #get_mission_coverage()
                    return render_template("index.html", is_admin=new_token)
                else:
                    session.pop('auth_token', None)
    except:
        pass
    return redirect(url_for("login_page"))


@app.route('/map/tables')
def table_page():
    return "Hi"


@app.route('/login', methods=["GET", "POST"])
def login_page():
    message = "none"
    try:
        try:
            if session["auth_token"]:
                valid, new_token = get_authenticate_data(session["auth_token"])
                if valid:
                    if new_token >= 1:
                        return redirect(url_for("home_page"))
                    else:
                        session.pop('auth_token', None)
        except:
            pass
        if request.method == "POST":
            email = request.form.get("emailInput").strip()
            password = request.form.get("passwordInput").strip()
            is_logged_in, status, u_id = login(email, password)
            if is_logged_in:
                session["auth_token"] = get_authenticate_token(app.config.get("SECRET_KEY"), u_id)
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
            reg = register(request.form.get("emailInput").strip(), request.form.get("passwordInput").strip(),
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
    return redirect(url_for('login_page'))


@app.route('/admin/dashboard', methods=["GET", "POST"])
def admin_page():
    try:
        if session["auth_token"]:
            valid, new_token = get_authenticate_data(session["auth_token"])
            if valid:
                if new_token == 2:
                    if request.method == "POST":
                        is_admin = 1 if request.form.get("is_admin") is not None else 0
                        genarate_unique_code(is_admin)
                    # auth_discover_bearer_token()
                    user_id = get_user_id_from_token(session["auth_token"])
                    name = get_user(user_id)[2]
                    codes = get_unique_codes()
                    return render_template("admin.html", name=name.capitalize(), codes=codes)
    except Exception as e:
        print(e)
    return render_template('404.html'), 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
