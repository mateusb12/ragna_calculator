from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField

from ragnarok.main.gear_query import generate_equipable_gear, get_cardlist_by_name
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

    headtop_choices = ['Ribbon']
    headmid_choices = ['No headgear']
    headlow_choices = ['No headgear']
    weapon_choices = ['No weapon']
    shield_choices = ['No shield']
    shoes_choices = ['No shoes']
    robe_choices = ['No robe']
    accessory_choices = ['No accessory']
    armor_choices = ['No armor']

    card_choices = ['Poring Card']

    base_level = SelectField('base_level', choices=baselevel_choices)
    job_level = SelectField('job_level', choices=joblevel_choices)
    class_name = SelectField('class_name', choices=class_choices)

    player_str = SelectField('player_str', choices=list(range(1, 100)))
    player_agi = SelectField('player_agi', choices=list(range(1, 100)))
    player_vit = SelectField('player_vit', choices=list(range(1, 100)))
    player_int = SelectField('player_int', choices=list(range(1, 100)))
    player_dex = SelectField('player_int', choices=list(range(1, 100)))
    player_luk = SelectField('player_int', choices=list(range(1, 100)))

    headtop_item = SelectField('headtop_item', choices=headtop_choices)
    headtop_refine = SelectField('headtop_refine', choices=list(range(1, 11)))
    headtop_card_list = SelectField('headtop_card_list', choices=card_choices)

    headmid_item = SelectField('headmid_item', choices=headmid_choices)
    headmid_refine = SelectField('headmid_refine', choices=list(range(1, 11)))
    headmid_card_list = SelectField('headmid_card_list', choices=card_choices)

    headlow_item = SelectField('headlow_item', choices=headlow_choices)
    headlow_refine = SelectField('headlow_refine', choices=list(range(1, 11)))
    headlow_card_list = SelectField('headlow_card_list', choices=card_choices)


    weapon_item = SelectField('headtop_item', choices=weapon_choices)
    shield_item = SelectField('headtop_item', choices=shield_choices)
    shoes_item = SelectField('headtop_item', choices=shoes_choices)
    armor_item = SelectField('armor_item', choices=armor_choices)
    robe_item = SelectField('armor_item', choices=robe_choices)
    accessory1_item = SelectField('armor_item', choices=accessory_choices)
    accessory2_item = SelectField('armor_item', choices=accessory_choices)


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

    equipable_list = generate_equipable_gear(form.class_name.data, form.base_level.data)

    form.headtop_item.choices = sorted(equipable_list['headtop'])
    form.headmid_item.choices = sorted(equipable_list['headmid'])
    form.headlow_item.choices = sorted(equipable_list['headlow'])
    form.weapon_item.choices = sorted(equipable_list['weapon'])
    form.shield_item.choices = sorted(equipable_list['shield'])
    form.shoes_item.choices = sorted(equipable_list['shoes'])
    form.armor_item.choices = sorted(equipable_list['shoes'])
    form.robe_item.choices = sorted(equipable_list['shoes'])
    form.accessory1_item.choices = sorted(equipable_list['accessory'])
    form.accessory2_item.choices = sorted(equipable_list['accessory'])

    form.headtop_card_list.choices = get_cardlist_by_name(form.headtop_item.data)
    form.headmid_card_list.choices = get_cardlist_by_name(form.headmid_item.data)
    form.headlow_card_list.choices = get_cardlist_by_name(form.headlow_item.data)
