import json
import os

from main.exporter import card_db
from model.equip_model import analyse_single_script

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'resources', "item_db_etc.json"))
a_file = open(db_path, "r")

json_object = json.load(a_file)

a_file.close()

# print(json_object)

aux = json_object['Body']['Body2']


# for q in json_object['Body']['Body2']:
#     print(q.keys())

def get_card_number(ctp: int) -> int:
    for h in range(len(aux)):
        if aux[h]['Id'] == ctp:
            return h

for p in range(4001, 4452):
    if p in card_db:
        script = card_db[p]['Script']
        name = card_db[p]['Name']
        card_id = card_db[p]['Id']
        if script != 0:
            p_script = script
            p_analysis = analyse_single_script(card_db[p]['Script'])
            print('id = {} analysis = {}'.format(card_id, p_analysis))
            desired_id = p
            picked_card = aux[get_card_number(desired_id)]
            picked_card['Script_adapted'] = p_analysis
            print('desired = {}'.format(picked_card))

a_file = open(db_path, "w")
json.dump(json_object, a_file)
a_file.close()
