from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password",
                             validators=[DataRequired(),
                                         Length(min=6,
                                                message="Password should be at least 6 characters long.")])
    remember_me = BooleanField("remember_me", validators=[])


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password",
                             validators=[DataRequired(),
                                         Length(min=6,
                                                message="Password should be at least 6 characters long.")])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(),
                                                                     EqualTo('password', "passwords do not match")
                                                                     ])

    email = StringField("email", validators=[DataRequired(), Email(message="Please type a valid email")])
    email_confirm = StringField("email_confirm", validators=[DataRequired(),
                                                             EqualTo("email", "Emails do not match")])
