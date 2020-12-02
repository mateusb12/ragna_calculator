from flask import Flask

app = Flask(__name__)

from pyflask.app.controllers import default
