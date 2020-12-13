from app import app, db
from flask import render_template, request, redirect
from app.models.forms import LoginForm, RegisterForm
from app.models.tables import User
import app.databases.db_operations as dbo
from sqlalchemy import exc


@app.route("/index/<user>")
@app.route("/", defaults={'user': None})
def index(user):
    return render_template('index.html',
                           user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
    else:
        print(form.errors)
    return render_template('login.html', form=form)


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
            else:
                created = False
                print("Ocorreu um erro. {}".format(flag))
                if 'email' in flag:
                    exist_email = True
                if 'username' in flag:
                    exist_username = True

    return render_template('sign_up.html', form=form, exist_email=exist_email, exist_username=exist_username)


@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    i = User("juliarizza2", "1234", "Julia Rizza3", "julia.rizza@gmail.com")
    db.session.add(i)
    db.session.commit()
    # try:
    #     db.session.add(i)
    #     return db.session.commit()
    # except exc.IntegrityError:
    #     print("houve exceção")
    #     db.session.rollback()
    return "ok"


@app.route("/about")
def about():
    return "<h1 style='color: red'>About!!!!</h1>"
