from flask import render_template, redirect, url_for, send_file, abort, jsonify, request
from flask_login import login_user, login_required, logout_user, current_user

from app.view import view_blueprint
from app.user.form.login import LoginForm, RegisterForm
from app.services.user import get_user_by_username_or_email, create_user, init_user_plan
from app.services.user import validate_email, validate_username
from app.util.captcha_tool import Captcha


@view_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username_or_email(form.username_or_email.data)
        login_user(user, form.remember.data)
        return redirect(url_for("user.home"))
    captcha = Captcha()
    form.captcha_id.data = captcha.captcha_id
    return render_template("login.html", form=form, captcha_id=captcha.captcha_id)


@view_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user and current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.email.data, form.password.data)
        init_user_plan(user, form.coupon.data or None)
        login_user(user, remember=True)
        return redirect(url_for("user.home"))
    captcha = Captcha()
    form.captcha_id.data = captcha.captcha_id
    return render_template("register.html", form=form, captcha_id=captcha.captcha_id)


@view_blueprint.route("/captcha")
def get_captcha():
    captcha = Captcha()
    return jsonify(dict(captcha_id=captcha.captcha_id))


@view_blueprint.route("/captcha/<captcha_id>")
def get_captcha_image(captcha_id):
    captcha = Captcha.get_by_captcha_id(captcha_id)
    if not captcha:
        abort(404)
    return send_file(captcha.image(), mimetype='image/png')


@view_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.login"))


@view_blueprint.route("/verification/email", methods=["POST"])
def verify_email():
    email = request.form.get("email")
    if email and validate_email(email):
        return jsonify(dict(message="success")), 200
    return jsonify(dict(message="email is illegal")), 400


@view_blueprint.route("/verification/username", methods=["POST"])
def verify_username():
    username = request.form.get("username")
    if username and validate_username(username):
        return jsonify(dict(message="success")), 200
    return jsonify(dict(message="username is illegal")), 400


@view_blueprint.route("/verification/captcha", methods=["POST"])
def verify_captcha():
    captcha_id = request.form.get("captcha_id")
    captcha_code = request.form.get("captcha_code")
    captcha = Captcha.get_by_captcha_id(captcha_id)
    if captcha and captcha.validate(captcha_code):
        return jsonify(dict(message="success")), 200
    return jsonify(dict(message="wrong captcha")), 400


