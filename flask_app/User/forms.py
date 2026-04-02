from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    BooleanField,
    EmailField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_app.models import User
from flask_app import bcrypt
from flask_login import current_user


class ProfileForm(FlaskForm):
    image = FileField("الصورة الشخصية", validators=[FileAllowed(["jpg", "png"])])
    first_name = StringField("أسم الأول", validators=[DataRequired()])
    last_name = StringField("أسم الأخير", validators=[DataRequired()])
    email = EmailField("أسم البريد الالكتروني", validators=[DataRequired(), Email()])
    phone = StringField(
        "رقم الهاتف", validators=[DataRequired(), Length(min=11, max=11)]
    )
    submit = SubmitField("تحديث الملف الشخصي")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError("That phone is taken. Please choose a different one.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("باسورد القديمة", validators=[DataRequired()])
    new_password = PasswordField("باسورد الجديدة", validators=[DataRequired()])
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
        if not any(char.isdigit() for char in new_password.data):
            raise ValidationError("Password must contain at least one number")

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.new_password.data:
            raise ValidationError("Passwords do not match")
