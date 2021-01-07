import json
import os
import pprint
import time

import pandas as pd

from main.exporter import card_db, equip_db


def categorize_scripts(input_path: str):
    script_table_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", input_path))

    with open(script_table_path) as json_file:
        input_scripts = json.load(json_file)

    return input_scripts


def adapt_ragnarok_to_python():
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "script_template.json"))
    return pd.read_json(r'{}'.format(script_path))['Body']


def analyse_small_script(small_script: str, script_json: pd.DataFrame):
    small_trim = small_script.split(";")
    small_trim = list(filter(None, small_trim))
    small_dict = dict()
    small_output = []
    for q in range(len(small_trim)):
        if q % 2 == 0:
            small_dict[small_trim[q]] = small_trim[q + 1]
    for a, b in small_dict.items():
        script_adapt_list = b.split(",")
        if a != "skill":
            adapted = script_json[script_adapt_list[0].lower()][0]
            script_adapt_list[0] = adapted
        else:
            adapted = "add_skill"
            script_adapt_list.insert(0, adapted)
        if a == "specialeffect2":
            adapted = "visual_effect"
            script_adapt_list.insert(0, adapted)
        small_output.append(tuple(script_adapt_list))

    if len(small_output) == 1:
        return small_output[0]
    else:
        return small_output


def default_analyser(script: str, script_json: pd.DataFrame):
    first_trim = script.replace(" ", ";").split(";")
    first_trim = list(filter(None, first_trim))
    if not script:
        return 'No Script'
    bonus_dict = dict()
    output_adapt = []
    if len(first_trim) == 3 and first_trim[-1] == "1":
        first_trim[-2] = first_trim[-2] + first_trim[-1]
        first_trim.pop()
    for q in range(len(first_trim)):
        if q % 2 == 0:
            bonus_dict[first_trim[q]] = first_trim[q + 1]
    for a, b in bonus_dict.items():
        script_adapt_list = b.split(",")
        if a != "skill":
            adapted = script_json[script_adapt_list[0].lower()][0]
            script_adapt_list[0] = adapted
        else:
            adapted = "add_skill"
            script_adapt_list.insert(0, adapted)
        output_adapt.append(tuple(script_adapt_list))

    if len(output_adapt) == 1:
        return output_adapt[0]
    else:
        return output_adapt


def repeated_analyser(script: str, script_json: pd.DataFrame):
    if not script:
        return 'No Script'
    first_trim = script.replace(" ", ";").split(";")
    first_trim = list(filter(None, first_trim))
    bonus_dict = {"bonus_extra": [], "bonus2_extra": [], "bonus3_extra": [], "bonus4_extra": [], "skill_extra": []}
    output_adapt = []
    for q in range(len(first_trim)):
        if q % 2 == 0:
            if first_trim[q] in bonus_dict:
                bonus_dict["{}_extra".format(first_trim[q])].append(first_trim[q + 1])
            else:
                bonus_dict[first_trim[q]] = first_trim[q + 1]
    clean_dict = bonus_dict.copy()
    for qx, qy in bonus_dict.items():
        if not qy:
            clean_dict.pop(qx, None)
        if len(qy) == 1:
            clean_dict[qx] = clean_dict[qx][0]
    for a, b in clean_dict.items():
        if type(b) is not list:
            script_adapt_list = b.split(",")
            if a not in ("skill", "skill_extra"):
                adapted = script_json[script_adapt_list[0].lower()][0]
                script_adapt_list[0] = adapted
            else:
                adapted = "add_skill"
                script_adapt_list.insert(0, adapted)
            output_adapt.append(tuple(script_adapt_list))
        else:
            for item in b:
                item_adapt_list = item.split(",")
                if a not in ("skill", "skill_extra"):
                    adapted = script_json[item_adapt_list[0].lower()][0]
                    item_adapt_list[0] = adapted
                else:
                    adapted = "add_skill"
                    item_adapt_list.insert(0, adapted)
                output_adapt.append(tuple(item_adapt_list))
    if len(output_adapt) == 1:
        return output_adapt[0]
    else:
        return output_adapt


def begin_analyser(script: str, script_json: pd.DataFrame):
    if not script:
        return 'No Script'
    first_trim = script.replace(" ", ";").replace(";{", "").replace(";;", ";").replace("}", "&") \
        .replace("if(", "if&").replace(";else", "else&").replace(");", "&").replace("){", "&").split("&")
    first_trim = list(filter(None, first_trim))
    if_else_dict = dict()
    for q in range(len(first_trim)):
        if first_trim[q] == "if":
            first_trim.insert(q + 2, "if_then")
    for w in range(len(first_trim)):
        if first_trim[w] == "if":
            if_else_dict['if'] = first_trim[w + 1]
        if first_trim[w] == "if_then":
            aux_then = analyse_small_script(first_trim[w + 1], script_json)
            if_else_dict['if_then'] = aux_then
        if first_trim[w] == "else":
            if_else_dict['else'] = analyse_small_script(first_trim[w + 1], script_json)

    return if_else_dict


def displaced_analyser(script: str, script_json: pd.DataFrame):
    if not script:
        return 'No Script'
    first_trim = script.replace(" ", ";").replace(";{", "").replace(";;", ";").replace("}", "&") \
        .replace("if(", "if&").replace(";else", "else&").replace(");", "&").replace("){", "&") \
        .replace(";if", "&if").split("&")
    first_trim = list(filter(None, first_trim))
    second_trim = first_trim.copy()
    if_else_dict = dict()
    for q in range(len(first_trim)):
        if first_trim[q] == "if":
            first_trim.insert(q + 2, "if_then")
            second_trim = first_trim.copy()
            if "if" not in first_trim[:q]:
                second_trim.insert(q - 1, "normal")
    if "normal" not in second_trim:
        second_trim.insert(0, "normal")
    for w in range(len(second_trim)):
        if second_trim[w] == "normal":
            if_else_dict['normal'] = analyse_small_script(second_trim[w + 1], script_json)
        if second_trim[w] == "if":
            if_else_dict['if'] = second_trim[w + 1]
        if second_trim[w] == "if_then":
            aux_then = analyse_small_script(second_trim[w + 1], script_json)
            if_else_dict['if_then'] = aux_then
        if second_trim[w] == "else":
            if_else_dict['else'] = analyse_small_script(second_trim[w + 1], script_json)
    return if_else_dict


def multipleif_analyser(script: str, script_json: pd.DataFrame):
    if not script:
        return 'No Script'
    first_trim = script.replace(" ", ";").replace(";{", "").replace(";;", ";").replace("}", "&") \
        .replace("if(", "if&").replace(";else", "else&").replace(");", "&").replace("){", "&") \
        .replace(";if", "&if").split("&")
    first_trim = list(filter(None, first_trim))
    second_trim = first_trim.copy()
    if_else_dict = dict()
    for q in range(len(first_trim)):
        if first_trim[q] == "if":
            first_trim.insert(q + 2, "if_then")
            second_trim = first_trim.copy()
            if "if" not in first_trim[:q]:
                second_trim.insert(q - 1, "normal")
    for w in range(len(second_trim)):
        if second_trim[w] == "if":
            if "if" not in if_else_dict:
                if_else_dict['if'] = second_trim[w + 1]
            else:
                wd = {"crowded": True, "amount": 2, "new_tag": "placeholder"}
                while wd["crowded"]:
                    wd["new_tag"] = "if_{}".format(wd["amount"])
                    if wd["new_tag"] in if_else_dict:
                        wd["amount"] += 1
                    else:
                        wd["crowded"] = False
                if_else_dict[wd["new_tag"]] = second_trim[w + 1]
        if second_trim[w] == "if_then":
            aux_then = analyse_small_script(second_trim[w + 1], script_json)
            if "if_then" not in if_else_dict:
                if_else_dict['if_then'] = aux_then
            else:
                wd = {"crowded": True, "amount": 2, "new_tag": "placeholder"}
                while wd["crowded"]:
                    wd["new_tag"] = "if_then_{}".format(wd["amount"])
                    if wd["new_tag"] in if_else_dict:
                        wd["amount"] += 1
                    else:
                        wd["crowded"] = False
                if_else_dict[wd["new_tag"]] = aux_then
    return if_else_dict


def autobonus_analyser(script: str, script_json: pd.DataFrame):
    if not script:
        return 'No Script'
    if_else_dict = dict()
    first_trim = script.replace(" ", ";").replace(";{", "").replace(";;", ";").replace("}", "&") \
        .replace("if(", "if&").replace(";else", "else&").replace(");", "&").replace("){", "&") \
        .replace(";if", "&if").replace(";autobonus", "&autobonus").replace(';"{;', "&").replace('"', "") \
        .replace("{;", "&").split("&")
    if first_trim[-1] == ";":
        first_trim.pop()
    for q in range(len(first_trim)):
        if first_trim[q] in ["autobonus", "autobonus2"]:
            first_trim.insert(q + 2, "autobonus_trigger")
            first_trim.insert(q + 4, "visual_effect")
    if "normal" not in first_trim:
        first_trim.insert(0, "normal")
    for w in range(len(first_trim)):
        if first_trim[w] == "normal":
            if_else_dict['normal'] = analyse_small_script(first_trim[w + 1], script_json)
        if first_trim[w] in ["autobonus", "autobonus2"]:
            if_else_dict['autobonus'] = analyse_small_script(first_trim[w + 1], script_json)
        if first_trim[w] == "autobonus_trigger":
            aux = first_trim[w + 1].split(",")
            if_else_dict['autobonus_trigger'] = list(filter(None, aux))

    return if_else_dict


def default_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['Default'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = default_analyser(script_desc, script_json)


def repeated_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['Repeated'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = repeated_analyser(script_desc, script_json)


def begin_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['Begin'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = begin_analyser(script_desc, script_json)


def displaced_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['Displaced'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = displaced_analyser(script_desc, script_json)


def multipleif_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['MultipleIf'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = multipleif_analyser(script_desc, script_json)


def autobonus_creator(dict_pack: dict):
    output_scripts = dict_pack['final_dict']
    input_scripts = dict_pack['input_scripts']
    script_json = dict_pack['script_json']
    for i, j in input_scripts['Autobonus'].items():
        script_id = i
        script_desc = j['Script']
        output_scripts[script_id] = autobonus_analyser(script_desc, script_json)


def assemble_json(input_file: str, output_file: str, **kwargs):
    final_dict = dict()
    input_script = categorize_scripts(input_file)
    script_json = adapt_ragnarok_to_python()
    dict_pack = {"final_dict": final_dict, "input_scripts": input_script, "script_json": script_json}
    autobonus_creator(dict_pack)
    multipleif_creator(dict_pack)
    displaced_creator(dict_pack)
    begin_creator(dict_pack)
    default_creator(dict_pack)
    repeated_creator(dict_pack)

    final_dict = dict(sorted(final_dict.items(), key=lambda x: x[0]))

    start_time = time.time()
    adapted_table_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", output_file))
    b_file = open(adapted_table_path, "w")
    json.dump(final_dict, b_file, indent=2)
    b_file.close()
    # pprint.pprint(final_dict)

    full_time = time.time() - start_time
    if full_time < 1:
        full_time *= 1000
        print("--- {} ms ---".format(round(full_time, 4)))
    else:
        print("--- {} seconds ---".format(full_time))

    print("JSON successfully dumped!")

    merge_card = kwargs.get('merge_card')
    merge_gear = kwargs.get('merge_gear')
    if merge_card:
        card_db_copy = card_db.copy()
        print(final_dict)
        for q in final_dict.keys():
            card_db_copy[int(q)]['Script_adapted'] = final_dict[q]
        final_dict = {"Header": {"Type": "ITEM_DB", "Version": 1}, "Body": {"Body2": list(card_db_copy.values())}}
        adapted_table_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", output_file))
        b_file = open(adapted_table_path, "w")
        json.dump(final_dict, b_file, indent=2)
        b_file.close()

    if merge_gear:
        gear_db_copy = equip_db.copy()
        for q in final_dict.keys():
            gear_db_copy[int(q)]['Script_adapted'] = final_dict[q]
        final_dict = {"Header": {"Type": "ITEM_DB", "Version": 1}, "Body": {"Body2": list(gear_db_copy.values())}}
        adapted_table_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "scripts", output_file))
        b_file = open(adapted_table_path, "w")
        json.dump(final_dict, b_file, indent=2)
        b_file.close()


assemble_json("gear_script_table.json", "gear_adapted_table.json", merge_gear=True)
# assemble_json("card_script_table.json", "card_adapted_table.json", merge_card=True)
