import json
import os

from main.exporter import card_db

# SITE SITE SITE
# O SITE TA AQUI

# https://jsonformatter.org/
from main.fixer.script_analyser import analyse_single_script

# db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'resources', "item_db_etc.json"))
# a_file = open(db_path, "r")
#
# json_object = json.load(a_file)
#
# a_file.close()

# print(json_object)

# aux = json_object['Body']['Body2']


# for q in json_object['Body']['Body2']:
#     print(q.keys())

def get_card_number(ctp: int) -> int:
    for h in range(len(aux)):
        if aux[h]['Id'] == ctp:
            return h


# for p in range(4001, 4452):
#     if p in card_db:
#         script = card_db[p]['Script']
#         name = card_db[p]['Name']
#         card_id = card_db[p]['Id']
#         if script != 0:
#             p_script = script
#             p_analysis = analyse_single_script(card_db[p]['Script'])
#             print('id = {} analysis = {}'.format(card_id, p_analysis))
#             desired_id = p
#             picked_card = aux[get_card_number(desired_id)]
#             picked_card['Script_adapted'] = p_analysis
#             print('desired = {}'.format(picked_card))


def generate_script_types():
    import json
    import pprint

    script_table_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", "script_table.json"))

    data = {"Begin": {}, "Displaced": {}, "Default": {}, "Repeated": {}}

    for qh in card_db:
        view_name = card_db[qh]['Name']
        view_card_id = card_db[qh]['Id']
        view_script = card_db[qh]['Script'].replace("\n", "")
        data_tuple = {"Name": view_name, "Id": view_card_id, "Script": view_script}
        if "if(" in view_script:
            if view_script[:3] == "if(":
                data['Begin'][view_card_id] = data_tuple
            else:
                data['Displaced'][view_card_id] = data_tuple
        else:
            set_check = card_db[view_card_id]['Script'].replace(",", " ").replace(";", " ").split(" ")
            set_check = list(filter(None, set_check))
            print('carta {} list_len {} set_len {} '.format(view_card_id, len(set_check), len(set(set_check))))
            if len(set_check) == len(set(set_check)):
                data['Default'][view_card_id] = data_tuple
            else:
                data['Repeated'][view_card_id] = data_tuple

    pprint.pprint(data)
    b_file = open(script_table_path, "w")
    json.dump(data, b_file, indent=2)
    b_file.close()

# NAO ATIVAR
# a_file = open(db_path, "w")
# json.dump(json_object, a_file)
# a_file.close()


generate_script_types()