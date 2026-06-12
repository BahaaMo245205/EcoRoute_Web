from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.auth.forms import (
    SignupForm,
    LoginForm,
    Reset_passwordForm,
    Forget_passwordForm,
)
from flask_app.models import User
from flask_app import db, bcrypt, mail
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


def sent_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="bebo245205@gmail.com",
        recipients=[user.email],
        body=f"""
        To reset your password, visit the following link:
        {url_for('auth.Reset_password', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        """,
    )
    mail.send(msg)


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("You have been logged in!", "success")
                next_page = request.args.get("next")
                return (
                    redirect(next_page) if next_page else redirect(url_for("main.home"))
                )
            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
                return redirect(url_for("auth.login"))
        else:
            for error in form.errors.values():
                flash(f"Error : {error[0]}", "danger")

    return render_template("auth_html/login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hash_pass = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                first_name=form.First_name.data,
                last_name=form.Last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                type_user=form.type_user.data,
                password=hash_pass,
            )
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully", "success")
            return redirect(url_for("auth.login"))
        else:
            for error in form.errors.values():
                flash(f"Error : {error[0]}", "danger")
            return redirect(url_for("auth.signup"))

    return render_template("auth_html/signup.html", form=form)


@auth.route("/Forget_password", methods=["GET", "POST"])
def Forget():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = Forget_passwordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            sent_reset_email(user)
            flash(
                "An email has been sent with instructions to reset your password.",
                "info",
            )
            return redirect(url_for("auth.login"))

    return render_template("auth_html/Forgetpassword.html", form=form)


@auth.route("/Reset_password/<path:token>", methods=["GET", "POST"])
def Reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("auth.Forget"))
    form = Reset_passwordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template(
        "auth_html/Reset_password.html", form=form, title="Reset Password"
    )


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
