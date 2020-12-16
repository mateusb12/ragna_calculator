import os
import sys

sys.path.append(sys.path[0][:-7] + 'ragnarok')

sys.path.append(sys.path[0][:-7] + 'ragnarok\model')

import pandas as pd
from flask import render_template, request, redirect, session, url_for, g

import app.databases.db_operations as dbo
from app import app
from app.models.forms import LoginForm, RegisterForm

# from ragnarok.model.statuspoints_evaluator import attribute_balance


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


@app.route("/calcframe")
def calcframe():
    jobnamelist = list(pd.read_csv('../ragnarok/resources/max_hp_table.csv').columns)[1:]
    for i in sys.path:
        print(i)
    # print("caminho = {}".format(sys.path[0][:-7] + 'ragnarok'))
    print("caminho atual = {}".format(os.path.abspath(os.path.join('..', 'default'))))
    return render_template('calculator_frame.html', jobnamelist=jobnamelist)


@app.route("/loginframe")
def loginframe():
    return render_template('frames/login_frame.html')


@app.route("/calctest")
def calctest():
    from app.controllers.html_functions import dynamic_choose
    joblist = list(pd.read_csv('../ragnarok/resources/max_hp_table.csv').columns)[1:]
    return render_template('frames/calctest.html',
                           joblist=joblist, dynamic_choose=dynamic_choose)
