import os
import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField

from app.models.extended_select_field import ExtendedSelectWidget, ExtendedSelectField

from ragnarok.model.equip_model import PlayerGear, Headgear
from ragnarok.main.gear_query import generate_equipable_gear, get_cardlist_by_name, dict_name_to_dict_id, \
    has_slots_by_name, generate_equipable_weapons
from ragnarok.main.exporter import jobname_list, job10, job50, job70, job99, equip_db


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

    refine_range = list(range(0, 11))

    headtop_choices = ['(No Headtop)']
    headmid_choices = ['(No Headmid)']
    headlow_choices = ['(No Headlow)']
    weapon_choices = ['(No Weapon)']
    shield_choices = ['(No Shield)']
    shoes_choices = ['(No Shoes)']
    robe_choices = ['(No Robe)']
    accessory1_choices = ['(No Accessory)']
    accessory2_choices = ['(No Accessory)']
    armor_choices = ['(No Armor)']

    card_choices = ['Poring Card']

    file_selector = SelectField('base_level', choices=["No file", "No file 2"])

    base_level = SelectField('base_level', choices=baselevel_choices)
    job_level = SelectField('job_level', choices=joblevel_choices)
    class_name = SelectField('class_name', choices=class_choices)
    player_gender = SelectField('player_gender', choices=['Male', 'Female'])

    player_str = SelectField('player_str', choices=list(range(1, 100)))
    player_agi = SelectField('player_agi', choices=list(range(1, 100)))
    player_vit = SelectField('player_vit', choices=list(range(1, 100)))
    player_int = SelectField('player_int', choices=list(range(1, 100)))
    player_dex = SelectField('player_int', choices=list(range(1, 100)))
    player_luk = SelectField('player_int', choices=list(range(1, 100)))

    headtop_item = SelectField(choices=headtop_choices)
    headtop_refine = SelectField(choices=refine_range)
    headtop_card_list = SelectField(choices=card_choices)

    headmid_item = SelectField(choices=headmid_choices)
    headmid_refine = SelectField(choices=refine_range)
    headmid_card_list = SelectField(choices=card_choices)

    headlow_item = SelectField(choices=headlow_choices)
    headlow_refine = SelectField(choices=refine_range)
    headlow_card_list = SelectField(choices=card_choices)

    shield_item = SelectField(choices=shield_choices)
    shield_refine = SelectField(choices=refine_range)
    shield_card_list = SelectField(choices=card_choices)

    shoes_item = SelectField(choices=shoes_choices)
    shoes_refine = SelectField(choices=refine_range)
    shoes_card_list = SelectField(choices=card_choices)

    armor_item = SelectField(choices=armor_choices)
    armor_refine = SelectField(choices=refine_range)
    armor_card_list = SelectField(choices=card_choices)

    robe_item = SelectField(choices=robe_choices)
    robe_refine = SelectField(choices=refine_range)
    robe_card_list = SelectField(choices=card_choices)

    accessory1_item = SelectField(choices=accessory1_choices)
    accessory1_refine = SelectField(choices=refine_range)
    accessory1_card_list = SelectField(choices=card_choices)

    accessory2_item = SelectField(choices=accessory2_choices)
    accessory2_refine = SelectField(choices=refine_range)
    accessory2_card_list = SelectField(choices=card_choices)

    # weapon_item = SelectField(choices=card_choices)

    weapon_item = ExtendedSelectField(
        choices=[
            ('No Weapon', (('(No Weapon)', '(No Weapon)'), ('(No Weapon)', '(No Weapon)')))
        ]
    )
    weapon_refine = SelectField(choices=refine_range)
    weapon_card_1 = SelectField(choices=card_choices)
    weapon_card_2 = SelectField(choices=card_choices)
    weapon_card_3 = SelectField(choices=card_choices)
    weapon_card_4 = SelectField(choices=card_choices)


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

    form.weapon_item.choices = generate_equipable_weapons(form.class_name.data, form.base_level.data)

    form.headtop_item.choices = sorted(equipable_list['headtop'])
    form.headmid_item.choices = sorted(equipable_list['headmid'])
    form.headlow_item.choices = sorted(equipable_list['headlow'])
    form.shield_item.choices = sorted(equipable_list['shield'])
    form.shoes_item.choices = sorted(equipable_list['shoes'])
    form.armor_item.choices = sorted(equipable_list['armor'])
    form.robe_item.choices = sorted(equipable_list['robe'])
    form.accessory1_item.choices = sorted(equipable_list['accessory'])
    form.accessory2_item.choices = sorted(equipable_list['accessory'])

    form.weapon_card_1.choices = sorted(get_cardlist_by_name(form.weapon_item.data))
    form.weapon_card_2.choices = sorted(get_cardlist_by_name(form.weapon_item.data))
    form.weapon_card_3.choices = sorted(get_cardlist_by_name(form.weapon_item.data))
    form.weapon_card_4.choices = sorted(get_cardlist_by_name(form.weapon_item.data))

    form.headtop_card_list.choices = sorted(get_cardlist_by_name(form.headtop_item.data))
    form.headmid_card_list.choices = sorted(get_cardlist_by_name(form.headmid_item.data))
    form.headlow_card_list.choices = sorted(get_cardlist_by_name(form.headlow_item.data))
    form.shield_card_list.choices = sorted(get_cardlist_by_name(form.shield_item.data))
    form.shoes_card_list.choices = sorted(get_cardlist_by_name(form.shoes_item.data))
    form.armor_card_list.choices = sorted(get_cardlist_by_name(form.armor_item.data))
    form.robe_card_list.choices = sorted(get_cardlist_by_name(form.robe_item.data))
    form.accessory1_card_list.choices = sorted(get_cardlist_by_name(form.accessory1_item.data))
    form.accessory2_card_list.choices = sorted(get_cardlist_by_name(form.accessory2_item.data))

    weapon_template = [form.weapon_item.data, form.weapon_refine.data,
                       "(No Card)", "(No Card)", "(No Card)", "(No Card)"]

    if form.weapon_card_1:
        weapon_template[2] = form.weapon_card_1.data
    if form.weapon_card_2:
        weapon_template[3] = form.weapon_card_2.data
    if form.weapon_card_3:
        weapon_template[4] = form.weapon_card_3.data
    if form.weapon_card_4:
        weapon_template[5] = form.weapon_card_4.data

    text_dict = {"headgear1": (form.headtop_item.data, form.headtop_refine.data, form.headtop_card_list.data),
                 "headgear2": (form.headmid_item.data, form.headmid_refine.data, form.headmid_card_list.data),
                 "headgear3": (form.headmid_item.data, form.headmid_refine.data, form.headmid_card_list.data),
                 "weapon": tuple(weapon_template),
                 "shield": (form.shield_item.data, form.shield_refine.data, form.shield_card_list.data),
                 "shoes": (form.shoes_item.data, form.shoes_refine.data, form.shoes_card_list.data),
                 "armor": (form.armor_item.data, form.armor_refine.data, form.armor_card_list.data),
                 "robe": (form.robe_item.data, form.robe_refine.data, form.robe_card_list.data),
                 "accessory1": (form.accessory1_item.data, form.accessory1_refine.data, form.accessory1_card_list.data),
                 "accessory2": (form.accessory2_item.data, form.accessory2_refine.data, form.accessory2_card_list.data)}

    gear_dict = dict_name_to_dict_id(text_dict)
    pe = PlayerGear(gear_dict, form.class_name.data, form.job_level.data)
    # if '(No Headtop)' in form.headtop_item.data:
    #     pe.unequip_noble_hats()
    #     headnames = pe.return_hat_dict_names()
    #     form.headtop_item.data = headnames['headtop']
    #     form.headmid_item.data = headnames['headmid']
    #     form.headlow_item.data = headnames['headlow']

    headnames = pe.return_hat_dict_names()

    if pe.has_noble_hats():
        form.headtop_item.data = headnames['headtop']
        form.headmid_item.data = headnames['headmid']
        form.headlow_item.data = headnames['headlow']

    if pe.weapon:
        if pe.weapon.two_handed:
            form.shield_item.data = "(No Shield)"

    form.base_level.default = '57'

    custombuild_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '..', '..', '..', 'ragnarok', 'resources',
                                                    "default_players"))

    custombuild_list = []

    for file in os.listdir(custombuild_path):
        sliced_file = file.split('.')
        if sliced_file[1] == 'json':
            custombuild_list.append((custombuild_path + "\\{}".format(file), sliced_file[0].capitalize()))

    form.file_selector.choices = custombuild_list
    # form.process()


def fill_calc_with_json(input_form):
    form = input_form
    txt_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..', '..', '..', 'ragnarok', 'resources',
                                            "default_players", "virtual_flag.txt"))
    f = open(txt_path, "r")
    flag_check = str(f.read())
    f.close()
    if flag_check == "True":
        f = open(txt_path, "w")
        f.write("False")
        f.close()
        custombuild = pd.read_json(r'{}'.format(form.file_selector.data))['Body']
        form.file_selector.default = custombuild['build_name']
        form.base_level.default = custombuild['base_level']
        form.class_name.default = custombuild['player_class']
        form.job_level.default = custombuild['job_level']

        form.player_str.default = custombuild['str']
        form.player_agi.default = custombuild['agi']
        form.player_vit.default = custombuild['vit']
        form.player_int.default = custombuild['int']
        form.player_dex.default = custombuild['dex']
        form.player_luk.default = custombuild['luk']

        form.headtop_item.default = custombuild['headgear1'][0]
        form.headtop_refine.default = custombuild['headgear1'][1]
        form.headtop_card_list.default = custombuild['headgear1'][2]

        form.headmid_item.default = custombuild['headgear2'][0]
        form.headmid_refine.default = custombuild['headgear2'][1]
        form.headmid_card_list.default = custombuild['headgear2'][2]

        form.headlow_item.default = custombuild['headgear3'][0]
        form.headlow_refine.default = custombuild['headgear3'][1]
        form.headlow_card_list.default = custombuild['headgear3'][2]

        form.shield_item.default = custombuild['shield'][0]
        form.shield_refine.default = custombuild['shield'][1]
        form.shield_card_list.default = custombuild['shield'][2]

        form.shoes_item.default = custombuild['shoes'][0]
        form.shoes_refine.default = custombuild['shoes'][1]
        form.shoes_card_list.default = custombuild['shoes'][2]

        form.armor_item.default = custombuild['armor'][0]
        form.armor_refine.default = custombuild['armor'][1]
        form.armor_card_list.default = custombuild['armor'][2]

        form.robe_item.default = custombuild['robe'][0]
        form.robe_refine.default = custombuild['robe'][1]
        form.robe_card_list.default = custombuild['robe'][2]

        form.accessory1_item.default = custombuild['accessory1'][0]
        form.accessory1_refine.default = custombuild['accessory1'][1]
        form.accessory1_card_list.default = custombuild['accessory1'][2]

        form.accessory2_item.default = custombuild['accessory2'][0]
        form.accessory2_refine.default = custombuild['accessory2'][1]
        form.accessory2_card_list.default = custombuild['accessory2'][2]

        form.weapon_item.default = custombuild['weapon'][0]
        form.weapon_refine.default = custombuild['weapon'][1]
        form.weapon_card_1.default = custombuild['weapon'][2]
        form.weapon_card_2.default = custombuild['weapon'][3]
        form.weapon_card_3.default = custombuild['weapon'][4]
        form.weapon_card_4.default = custombuild['weapon'][5]
        form.process()


    return 'OI MEU CHAPA TUDO BOM COM VC'
