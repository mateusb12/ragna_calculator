# %run gear_db.ipynb
from model.decorador_db_gen import DbGenerator
import yaml
import math
import pandas as pd
import logging
import os


def open_json(filename):
    foldername = 'resources'
    dir_path = os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(foldername)
    with open(r'{}\\{}'.format(dir_path, filename)) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

