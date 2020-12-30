# %run gear_db.ipynb
from ragnarok.model.build_model import PlayerBuild
from ragnarok.model.decorador_db_gen import DbGenerator

# import yaml
import os
import sys
import pandas as pd
import time

start_time = time.time()


# def open_yml(filename):
#     folder_name = 'resources'
#     dir_path = os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(folder_name)
#     with open(r'{}\\{}'.format(dir_path, filename)) as file:
#         return yaml.load(file, Loader=yaml.FullLoader)


def open_json(filename: str) -> pd.DataFrame:
    folder_name = 'resources'
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder_name, filename))
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

p1 = PlayerBuild(jbl, 99, 70, 'gypsy', [18, 68, 42, 28, 42, 65])
p1.print_build()

print(p1.export_build())

print("\n\n")
full_time = time.time() - start_time
if full_time < 1:
    full_time *= 1000
    print("--- {} ms ---".format(round(full_time, 4)))
else:
    print("--- {} seconds ---".format(full_time))

import pyHook

pizza = {"headgear1": ["Poo Poo Hat", 0, "(No Card)"],
         "headgear2": ["Sunglasses [1]", 0, "Nightmare Card"],
         "headgear3": ["Gentleman's Pipe", 0, "(No Card)"],
         "shield": ["Guard [1]", 0, "Thara Frog Card"],
         "shoes": ["Crystal Pumps", 0, "(No Card)"],
         "armor": ["Formal Suit [1]", 0, "Marc Card"],
         "robe": ["Ragamuffin Manteau", 0, "(No Card)"],
         "accessory1": ["Rosary [1]", 0, "Smokie Card"],
         "accessory2": ["Rosary", 0, "(No Card)"],
         "weapon": ["(no weapon)", 0, "(No Card)", "(No Card)", "(No Card)", "(No Card)"]}
