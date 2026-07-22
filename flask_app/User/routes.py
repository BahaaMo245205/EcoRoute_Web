from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.User.forms import ProfileForm, ChangePasswordForm
from flask_login import login_required, current_user
from flask_app.User.helpr import save_picture
from flask_app.models import Car, User
from flask_app import db, bcrypt

user_routes = Blueprint(
    "user_routes", __name__, template_folder="templates", static_folder="static"
)


@user_routes.route("/Profile", methods=["GET", "POST"])
@login_required
def profile():
    car = Car.query.filter_by(user_id=current_user.user_id).all()

    return render_template("user/Profile.html", cars=car)


@user_routes.route("/UpdateProfile", methods=["GET", "POST"])
@login_required
def UpdateProfile():
    form = ProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if form.image.data:
                picture_file = save_picture(form.image.data)
                user.image = picture_file

            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.phone = form.phone.data

            db.session.commit()
            flash("تم تحديث بيانات ملفك الشخصي بنجاح", "success")
            return redirect(url_for("user_routes.profile"))
        else:
            for error in form.errors.values():
                flash(error[0], "danger")
            return redirect(url_for("user_routes.UpdateProfile"))

    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone.data = str(current_user.phone)
        form.image.data = current_user.image

    return render_template("user/UpdateProfile.html", form=form)


# Change Password
@user_routes.route("/ChangePassword", methods=["GET", "POST"])
@login_required
def ChangePassword():
    form = ChangePasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if bcrypt.check_password_hash(
                current_user.password, form.old_password.data
            ):
                hash_password = bcrypt.generate_password_hash(form.new_password.data)
                current_user.password = hash_password
                db.session.commit()
                flash("تم تغيير كلمة المرور بنجاح", "success")
                return redirect(url_for("user_routes.profile"))
            else:
                flash("كلمة المرور القديمة غير صحيحة", "danger")
                return redirect(url_for("user_routes.ChangePassword"))
    return render_template("user/ChangePassword.html", form=form)
