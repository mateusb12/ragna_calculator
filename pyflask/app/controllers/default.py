from app import app
from flask import render_template
from app.models.forms import LoginForm


@app.route("/index/<user>")
@app.route("/", defaults={'user': None})
def index(user):
    return render_template('index.html',
                           user=user)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

# @app.route("/test", defaults={'name': None})
# @app.route("/test/<name>")
# def test(name=None):
#     if name:
#         return "Hello, {}".format(name)
#     else:
#         return "Hello!"
