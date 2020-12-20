from typing import List

import pandas as pd
import os


def open_json(filename: str) -> pd.DataFrame:
    folder_name = 'resources'
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder_name, filename))
    return pd.read_json(r'{}'.format(dir_path))


def uncapitalize(s):
    return s[0].lower() + s[1:]


jbl = open_json('job_bonuses.json')

jobname_list = list(jbl.columns.values)

aux = jobname_list.copy()
aux.remove('novice')
aux.remove('super_novice')

job10 = ['novice']
job50 = aux
job99 = ['super_novice']

testedf = pd.read_csv(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'stat_points_table.csv')))

maxjob_table = {'novice': 10,
                'super_novice': 99,
                'swordsman': 50,
                'mage': 50,
                'archer': 50,
                'acolyte': 50,
                'merchant': 50,
                'thief': 50,
                'knight': 50,
                'priest': 50,
                }

import math
