# from pyflask.app import app
# from pyflask.app import manager
from app import app
from app import manager
import sys
from os.path import abspath, dirname
# python -m comando

if __name__ == "__main__":
    app.run(host="localhost")
