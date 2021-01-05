import os

from main.exporter import card_db


def generate_script_types():
    import json
    import pprint

    script_table_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", "script_table.json"))

    data = {"Begin": {}, "Displaced": {}, "Default": {}, "Repeated": {}, "Autobonus": {}, "MultipleIf": {}}

    for qh in card_db:
        view_name = card_db[qh]['Name']
        view_card_id = card_db[qh]['Id']
        view_script = card_db[qh]['Script'].replace("\n", "")
        data_tuple = {"Name": view_name, "Id": view_card_id, "Script": view_script}
        if "if(" in view_script:
            if view_script[:3] == "if(":
                if view_script.count("if") == 1:
                    data['Begin'][view_card_id] = data_tuple
                else:
                    data['MultipleIf'][view_card_id] = data_tuple
            else:
                data['Displaced'][view_card_id] = data_tuple
        else:
            if 'autobonus' in view_script:
                data['Autobonus'][view_card_id] = data_tuple
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
