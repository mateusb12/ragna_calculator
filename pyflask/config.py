import os.path

DEBUG = True
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///storage.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'um-nome-bem-seguro'
