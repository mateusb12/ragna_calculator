from app import app, db
from flask import render_template, request, redirect
from app.models.forms import LoginForm, RegisterForm
from app.models.tables import User
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
    return render_template('login.html', form=form)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
        print(form.email.data)

        if request.method == "POST":
            # new_user = User(form.username.data, form.password.data, "Pedro", form.email.data)
            # db.session.add(new_user)
            # db.session.commit()
            print("Adicionado ao database!")
        else:
            pass
    return render_template('sign_up.html', form=form)


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
