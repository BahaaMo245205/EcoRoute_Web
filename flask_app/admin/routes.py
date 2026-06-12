from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_app import admin_dashboard, db, bcrypt
from flask_app.models import User, Car, Trip, Bookings


class UserModelView(ModelView):
    can_create = True
    can_edit = False
    can_delete = False
    can_view_details = True
    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password).decode("utf-8")


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (
            current_user.type_user == "Admin" or current_user.user_id == 1
        )


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and (
            current_user.type_user == "Admin" or current_user.user_id == 1
        )


adminbp = Blueprint(
    "adminbp", __name__, template_folder="templates", static_folder="static"
)

admin_dashboard.add_view(UserModelView(User, db.session))
admin_dashboard.add_view(MyModelView(Car, db.session))
admin_dashboard.add_view(MyModelView(Trip, db.session))
admin_dashboard.add_view(MyModelView(Bookings, db.session))
