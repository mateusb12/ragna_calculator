import os
import sys
from pathlib import Path

sys.path.append(sys.path[0][:-7])

import pandas as pd
from flask import render_template, request, redirect, session, url_for, g

import app.databases.db_operations as dbo
from app import app
from app.models.forms import LoginForm, RegisterForm, CalculatorForm, calc_dynamic_select

from ragnarok.main.gear_query import is_refineable, has_slots, has_slots_by_name, is_refineable_by_name, \
    normalize_form_values

from ragnarok.model.statuspoints_evaluator import attribute_balance
from ragnarok.model.build_model import PlayerBuild
from ragnarok.resources.interface.interface_generator import InterfaceGenerator


# cur_path = os.path.abspath(os.curdir)


def open_json(filename):
    cur_path = str(Path(__file__).parents[3]) + "\\ragnarok\\resources\\" + filename
    return pd.read_json(cur_path)


from ragnarok.main.exporter import jbl, uncapitalize


@app.route("/index/<user>")
@app.route("/", defaults={'user': None})
def index(user):
    return render_template('index.html',
                           user=user)


@app.route("/base")
def base():
    return render_template('base.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for('protected'))
    form = LoginForm()
    login_error = None
    info = None
    if form.validate_on_submit():
        if request.method == "POST":
            session.pop('user', None)
            flag = dbo.UserDB.login(form.username.data, form.password.data)
            print(flag)
            if flag:
                session['user'] = request.form['username']
                # info = dbo.UserDB.user_query('username', form.username.data)[0]
                return redirect(url_for('protected'))
            else:
                login_error = True
    else:
        print(form.errors)
    return render_template('login.html', form=form, login_error=login_error)


@app.route("/protected")
def protected():
    if g.user:
        info = dbo.UserDB.user_query('username', session['user'])[0]
        return render_template('profile.html', user=session['user'], info=info)
    return redirect(url_for('index'))


@app.route("/protected/calc")
def calculator():
    if g.user:
        return render_template('calculator.html', user=session['user'])
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']


@app.route("/dropsession")
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = RegisterForm()
    created = None
    exist_email = None
    exist_username = None
    if form.validate_on_submit():
        if request.method == "POST":
            username = form.username.data
            password = form.password.data
            email = form.email.data
            flag = dbo.User.create(username, password, email)
            if type(flag) == bool and flag == True:
                created = True
                print("Cadastrado com sucesso!")
                return redirect(url_for('login'))
            else:
                created = False
                print("Ocorreu um erro. {}".format(flag))
                if 'email' in flag:
                    exist_email = True
                if 'username' in flag:
                    exist_username = True

    return render_template('sign_up.html', form=form, exist_email=exist_email,
                           exist_username=exist_username, created=created)


@app.route("/about")
def about():
    return "<h1 style='color: red'>About!!!!</h1>"


@app.route("/calcframe", methods=["POST", "GET"])
def calcframe():
    form = CalculatorForm()
    pi = request.form.to_dict()
    complex_info = 0
    if 'csrf_token' in pi:
        del pi['csrf_token']
    pi['complex_info'] = 'none'
    if request.method == 'POST' and request.form:
        calc_dynamic_select(form)
        p1 = PlayerBuild(jbl, int(pi['base_level']), int(pi['job_level']), uncapitalize(pi['class_name']),
                         [int(pi['player_str']), int(pi['player_agi']), int(pi['player_vit']),
                          int(pi['player_int']), int(pi['player_dex']), int(pi['player_luk'])])
        gear_skeleton = normalize_form_values(pi)
        pi['complex_info'] = p1.export_build()
        igen = InterfaceGenerator(p1)
        igen.generate_interface()
        # tt = {"headgear1": ('(No Headtop)', 0, 0),
        #       "headgear2": ('Sunglasses [1]', 0, 'Willow Card'),
        #       "headgear3": ('Cigarette', 0, 0),
        #       "weapon": None,
        #       "shield": ('Buckler [1]', 0, 'Thief Bug Egg Card'),
        #       "shoes": ('Sandals [1]', 0, 'Matyr Card'),
        #       "armor": ('Formal Suit [1]', 0, 'Dokebi Card'),
        #       "robe": ('Hood [1]', 0, 'Condor Card'),
        #       "accessory1": ('Clip [1]', 0, 'Sage Worm Card'),
        #       "accessory2": ('Silver Ring', 0, 0)}
        # igen.generate_equip_details(tt, 'female')
        igen.generate_equip_details(gear_skeleton, 'female')
    return render_template('calculator_frame.html',
                           form=form,
                           player_info=pi,
                           image_url='static/assets/custom.png',
                           is_refineable=is_refineable,
                           has_slots=has_slots)


@app.route("/loginframe")
def loginframe():
    return render_template('frames/login_frame.html')


@app.route("/csvtest")
def csvtest():
    return render_template('frames/csvtest.html')


@app.route("/calctest", methods=["POST", "GET"])
def calctest():
    from app.controllers.html_functions import dynamic_choose, test_function
    form = CalculatorForm()
    exports = request.form.to_dict()
    if 'csrf_token' in exports:
        del exports['csrf_token']
    if request.method == 'POST' and request.form:
        calc_dynamic_select(form)
        print(form.class_name)

    joblist = list(pd.read_csv('../ragnarok/resources/max_hp_table.csv').columns)[1:]
    return render_template('frames/calctest.html',
                           form=form,
                           joblist=joblist,
                           dynamic_choose=dynamic_choose,
                           exports=exports)
