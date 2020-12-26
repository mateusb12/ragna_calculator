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


def is_equipable(player_job: str, player_level: int, ch: dict):
    if player_job.lower() == 'super_novice':
        player_job = 'SuperNovice'

    if 'Upper' in ch['Classes'].keys():
        if player_job.lower() not in job70:
            return False, 'Transclass only'

    if player_job.lower() in job70:
        player_job = job_adapt['Body'][player_job]

    if 'All' in ch['Jobs'].keys():
        if player_job.lower() in map(lambda x: x.lower(), ch['Jobs'].keys()):
            return False, ch['Jobs'].keys()
    else:
        if player_job.lower() not in map(lambda x: x.lower(), ch['Jobs'].keys()):
            return False, ch['Jobs'].keys()

    if 'EquipLevelMin' in ch:
        if int(player_level) <= int(ch['EquipLevelMin']):
            return False, 'Levelmin: {}'.format(ch['EquipLevelMin'])

    return True, ch


# print(is_equipable('super_novice', 88, hat_db[2289]))


