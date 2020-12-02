from pyflask.app import app


@app.route("/")
def index():
    return "Hello World!"
