from app import app
from flask import render_template


@app.route("/index/<user>")
@app.route("/", defaults={'user': None})
def index(user):
    return render_template('index.html',
                           user=user)

# @app.route("/test", defaults={'name': None})
# @app.route("/test/<name>")
# def test(name=None):
#     if name:
#         return "Hello, {}".format(name)
#     else:
#         return "Hello!"
