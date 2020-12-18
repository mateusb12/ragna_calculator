import pandas as pd
import os


def open_json(filename: str) -> pd.DataFrame:
    folder_name = 'resources'
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder_name, filename))
    return pd.read_json(r'{}'.format(dir_path))


jbl = open_json('job_bonuses.json')


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
