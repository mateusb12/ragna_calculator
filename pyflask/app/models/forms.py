from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField
from ragnarok.main.exporter import jobname_list, job10, job50, job70, job99


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


class CalculatorForm(FlaskForm):
    baselevel_choices = list(range(1, 100))
    joblevel_choices = [1]
    class_choices = [i.capitalize() for i in jobname_list]

    base_level = SelectField('base_level', choices=baselevel_choices)
    job_level = SelectField('job_level', choices=joblevel_choices)
    class_name = SelectField('class_name', choices=class_choices)

    player_str = SelectField('player_str', choices=list(range(1, 100)))
    player_agi = SelectField('player_agi', choices=list(range(1, 100)))
    player_vit = SelectField('player_vit', choices=list(range(1, 100)))
    player_int = SelectField('player_int', choices=list(range(1, 100)))
    player_dex = SelectField('player_int', choices=list(range(1, 100)))
    player_luk = SelectField('player_int', choices=list(range(1, 100)))


def calc_dynamic_select(input_form):
    form = input_form
    if form.class_name.data in [i.capitalize() for i in job10]:
        form.job_level.choices = list(range(1, 11))
    if form.class_name.data in [i.capitalize() for i in job50]:
        form.job_level.choices = list(range(1, 51))
    if form.class_name.data in [i.capitalize() for i in job70]:
        form.job_level.choices = list(range(1, 71))
    if form.class_name.data in [i.capitalize() for i in job99]:
        form.job_level.choices = list(range(1, 100))
