# %run gear_db.ipynb
from model.build_model import PlayerBuild
from model.decorador_db_gen import DbGenerator
# import yaml
import os
import pandas as pd

# def open_yml(filename):
#     folder_name = 'resources'
#     dir_path = os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(folder_name)
#     with open(r'{}\\{}'.format(dir_path, filename)) as file:
#         return yaml.load(file, Loader=yaml.FullLoader)


def open_json(filename):
    folder_name = 'resources'
    dir_path = (os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(folder_name)) + filename
    return pd.read_json(r'{}'.format(dir_path))


jbl = open_json('job_bonuses.json')
eql = open_json('item_db_equip.json')

dbg = DbGenerator(eql)

equip_db = dbg.get_equip_db()

weapon_db = dbg.get_weapon_db()
hat_db = dbg.get_hat_db()
shield_db = dbg.get_shield_db()
robe_db = dbg.get_robe_db()
armor_db = dbg.get_armor_db()
shoes_db = dbg.get_shoes_db()
accessory_db = dbg.get_accessory_db()

db_package = (weapon_db, hat_db, shield_db, robe_db, armor_db, shoes_db, accessory_db)

p1 = PlayerBuild(jbl, 99, 50, 'knight', [1, 1, 1, 1, 1, 1])
p1.print_build()
