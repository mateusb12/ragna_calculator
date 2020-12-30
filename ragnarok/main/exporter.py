import math
import textwrap
from typing import List, Tuple

import pandas as pd
import os

from ragnarok.model.decorador_db_gen import DbGenerator
from ragnarok.resources.interface.card_desc import pandas_to_dict


def open_json(filename: str) -> pd.DataFrame:
    folder_name = 'resources'
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', folder_name, filename))
    return pd.read_json(r'{}'.format(dir_path))


def uncapitalize(s):
    return s[0].lower() + s[1:]


jbl = open_json('job_bonuses.json')

adjective_df = pd.read_csv(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'resources', 'card_adjectives.csv')))

adjective_list = pandas_to_dict(adjective_df)

jobname_list = list(jbl.columns.values)

aux = jobname_list.copy()
aux.remove('novice')
aux.remove('super_novice')

job10 = ['novice']
job50 = []
job70 = []
job99 = ['super_novice']

for i, j in jbl.items():
    if j['MAX_JOB'] == 50:
        job50.append(i)
    if j['MAX_JOB'] == 70:
        job70.append(i)

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

cdb = open_json('item_db_etc.json')

card_db = dict()

for i in cdb['Body']['Body2']:
    if i['Type'] == 'Card' and 'Locations' in i:
        card_db[int(i['Id'])] = i

db_package = (weapon_db, hat_db, shield_db, robe_db, armor_db, shoes_db, accessory_db, equip_db, card_db)

job_adapt = open_json('job_adaptation.json')
script_set = set()
first_param_set = set()
second_param_set = set()

# script_json = open_json("script_template.json")

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', "script_template.json"))
script_json = pd.read_json(r'{}'.format(script_path))

for i in equip_db:
    aux = equip_db[i]
    if 'Script' not in aux:
        pass
        # print('Name: {}, Script: {}'.format(equip_db[i]['Name'], ['No Script']))
    else:
        script = str(equip_db[i]['Script'])
        fragmented = script.split(';')

        sliced = fragmented[0].split(' ')
        formatted = sliced
        first_param = sliced[0]

        if first_param == '/*':
            first_param = fragmented[0].split(' ')[1]
        if first_param == '0':
            first_param = "No Script"
            formatted = ["No Script"]
        if first_param[0:2] == 'if':
            aux_list = fragmented[0].split(' ')[2:]

        if len(formatted) != 1:
            second_param_set.add(formatted[1])
            # print('ae {} ({})'.format(formatted, len(formatted)))

        first_param_set.add(first_param)
        # print('Script: ({}) {}'.format(first_param, fragmented))
        for q in fragmented:
            script_set.add(q)

for h in sorted(second_param_set):
    print(h)
