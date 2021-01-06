import os

from main.exporter import card_db, equip_db


def generate_script_types(main_db: dict, output_file: str):
    import json
    import pprint

    script_table_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", output_file))

    data = {"Begin": {}, "Displaced": {}, "Default": {}, "Repeated": {}, "Autobonus": {}, "MultipleIf": {}}

    for qh in main_db:
        view_name = main_db[qh]['Name']
        view_item_id = main_db[qh]['Id']
        if 'Script' not in main_db[qh]:
            main_db[qh]['Script'] = ""
        first_script = main_db[qh]['Script']
        if first_script == 0:
            first_script = ""
        view_script = first_script.replace("\n", "")
        data_tuple = {"Name": view_name, "Id": view_item_id, "Script": view_script}
        if "if(" in view_script:
            if view_script[:3] == "if(":
                if view_script.count("if") == 1:
                    data['Begin'][view_item_id] = data_tuple
                else:
                    data['MultipleIf'][view_item_id] = data_tuple
            else:
                data['Displaced'][view_item_id] = data_tuple
        else:
            if 'autobonus' in view_script:
                data['Autobonus'][view_item_id] = data_tuple
            else:
                raw_script = main_db[view_item_id]['Script']
                if raw_script == 0:
                    raw_script = ""
                set_check = raw_script.replace(",", " ").replace(";", " ").split(" ")
                set_check = list(filter(None, set_check))
                print('carta {} list_len {} set_len {} '.format(view_item_id, len(set_check), len(set(set_check))))
                if len(set_check) == len(set(set_check)):
                    data['Default'][view_item_id] = data_tuple
                else:
                    data['Repeated'][view_item_id] = data_tuple

    pprint.pprint(data)
    b_file = open(script_table_path, "w")
    json.dump(data, b_file, indent=2)
    b_file.close()


# NAO ATIVAR
# a_file = open(db_path, "w")
# json.dump(json_object, a_file)
# a_file.close()


# generate_script_types(card_db, "script_table2.json")
generate_script_types(equip_db, "gear_script_table.json")
