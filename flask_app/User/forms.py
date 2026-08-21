import re

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flask_app import bcrypt


class ProfileForm(FlaskForm):
    image = FileField(
        "الصورة الشخصية", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    first_name = StringField("أسم الأول", validators=[DataRequired()])
    last_name = StringField("أسم الأخير", validators=[DataRequired()])
    email = EmailField("أسم البريد الالكتروني", validators=[DataRequired(), Email()])
    phone = StringField(
        "رقم الهاتف", validators=[DataRequired(), Length(min=10, max=11)]
    )
    submit = SubmitField("تحديث الملف الشخصي")

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError("That email is taken. Please choose a different one.")

    # def validate_phone(self, phone):
    #     user = User.query.filter_by(phone=phone.data).first()
    #     if user:
    #         raise ValidationError("That phone is taken. Please choose a different one.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("باسورد القديمة", validators=[DataRequired()])
    new_password = PasswordField(
        "باسورد الجديدة", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "أكد الباسورد جديد", validators=[DataRequired(), EqualTo("new_password")]
    )
    show = BooleanField("Show me password")
    submit = SubmitField("تـحديث الباسورد")

    def validate_old_password(self, old_password):
        if not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError("Password incorrect")

    def validate_new_password(self, new_password):
        if len(new_password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not re.search("[a-z]", new_password.data):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search("[A-Z]", new_password.data):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search('[!@#$%^&*(),.?":{}|<>]', new_password.data):
            raise ValidationError(
                "Password must contain at least one special character"
            )

        if not any(char.isdigit() for char in new_password.data):
            raise ValidationError("Password must contain at least one number")

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.new_password.data:
            raise ValidationError("Passwords do not match")
