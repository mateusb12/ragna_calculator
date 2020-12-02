from flask import Flask
import sqlalchemy

app = Flask(__name__)

from pyflask.app.controllers import default
