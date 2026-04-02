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
from flask_app.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    show = BooleanField("Show me password")
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    First_name = StringField("First Name", validators=[DataRequired()])
    Last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=11)])
    type_user = SelectField(
        "Type", validators=[DataRequired()], choices=["Riders", "Users"]
    )
    password = PasswordField(
        "password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[DataRequired(), Length(min=8, max=20), EqualTo("password")],
    )
    show = BooleanField("Show me password")
    submit = SubmitField("Signup")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError("That phone is taken. Please choose a different one.")


class Reset_passwordForm(FlaskForm):
    password = PasswordField(
        "باسورد جدید", validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm_password = PasswordField(
        "تأكد من الباسورد",
        validators=[DataRequired(), Length(min=8, max=20), EqualTo("password")],
    )
    show = BooleanField("Show me password")
    submit = SubmitField("تغیر باسورد")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if self.password.data != self.confirm_password.data:
            raise ValidationError("Passwords do not match.")


class Forget_passwordForm(FlaskForm):
    email = EmailField("ایمیل", validators=[DataRequired(), Email()])
    submit = SubmitField("ارسال")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(
                "There is no account with that email. You must register first."
            )
