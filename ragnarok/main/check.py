# %run gear_db.ipynb
import yaml
import pandas as pd
import os


def open_json(filename):
    foldername = 'resources'
    dir_path = os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(foldername)
    with open(r'{}\\{}'.format(dir_path, filename)) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


ab = pd.read_csv('../resources/max_hp_table.csv')


def soma(a: int, b: int) -> int:
    return a + b


print(soma.__annotations__)
