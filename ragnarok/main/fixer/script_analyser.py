import os
from typing import List

import pandas as pd

from main.exporter import card_db


def analyse_single_script(input_script: str):
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'resources', "script_template.json"))
    script_json = pd.read_json(r'{}'.format(script_path))['Body']
    if_else_dict = dict()
    current_script = input_script.replace("\n", "")
    if_flag = False
    if str(current_script) != "0":
        if "if(" in current_script:
            if_flag = True
            compact = current_script.split("if")
            compact.pop(0)
            if_count = current_script.count("if")
            if if_count == 1:
                simple_trim = current_script.replace("if(", "").replace(" { ", "|")\
                    .replace(" }", "").replace(")", "").replace("(", "")
                compact = simple_trim.split("|")
                print('compacto {} mano {}'.format(compact, current_script))
                adapted_if = if_analysis(compact[0])
                adapted_then = small_analysis(compact[1], script_json)
                if_else_dict["condition_1"] = {"if": adapted_if, "then": adapted_then}
            else:
                occurrences = current_script.count("if")
                for qh in range(len(compact)):
                    position = qh + 1
                    content = compact[qh].replace("||", "[or]").replace(") bonus", "|bonus") \
                        .replace(" { ", "|").replace(" } ", "").replace(" }", "").replace("{ ", "|").split("|")
                    content_if = content[0]
                    content_then = content[1]
                    adapted_if = if_analysis(content_if)
                    adapted_then = small_analysis(content_then, script_json)
                    if_else_dict["condition{}".format(position)] = {"if": adapted_if, "then": adapted_then}
        if "autobonus" in current_script:
            return 'AUTOBONUS SCRIPT'

        if if_flag:
            return if_else_dict
        else:
            return small_analysis(input_script, script_json)

        # print("dict = {}".format(dict_script))


def if_analysis(if_script: str):
    if "readparam" in if_script:
        return if_script.replace("(readparam", "player").replace("(b", "_").replace(")", "").lower()
    if "refine" in if_script:
        trimmed_if = if_script.replace("getrefine", "refine")
        return trimmed_if
    if "BaseClass" in if_script:
        if "[or]" in if_script:
            trimmed_if = if_script.replace("[or]BaseClass", "").replace("BaseClass==", "")
            return "player_job in {}".format(trimmed_if.split("=="))
        job_bank = []
        trimmed_if = if_script.split("||")
        for q in trimmed_if:
            job_bank.append(q.split("==")[1].replace(")", ""))
        return 'player_job in {}'.format(job_bank)
    if "isequipped" in if_script:
        trimmed_if = if_script.replace("!isequipped", "").replace(")", "").replace("((", "").split(",")
        return 'combo_equipped {}'.format(trimmed_if)


def small_analysis(small_script: str, script_json: dict):
    dict_script = dict()
    dict_script['bonus_extra'] = []
    dict_script['bonus2_extra'] = []
    dict_script['bonus3_extra'] = []
    dict_script['skill_extra'] = []
    dict_script['Skill_extra'] = []
    script_function = []
    first_split = small_script.split(' ')
    first_split = [s.replace('\n', '') for s in first_split]

    if not first_split[-1]:
        first_split.pop()
    for q in range(len(first_split)):
        # print('q = {} dict(q) = {}'.format(q, first_split[q]))
        if q % 2 == 0:
            if first_split[q] not in dict_script:
                dict_script[first_split[q]] = first_split[q + 1]
            else:
                dict_script['{}_extra'.format(first_split[q])].append(first_split[q + 1])

    if 'bonus2' in dict_script:
        bonus2 = dict_script['bonus2'].split(',')
        bonus2_sufix = bonus2[0]
        bonus2_type = bonus2[1]
        bonus2_value = bonus2[2][:-1].replace(';', '')

        script_function.append((script_json[bonus2_sufix.lower()][0], bonus2_type, bonus2_value))

    if 'bonus' in dict_script:
        bonus = dict_script['bonus'].replace(';', '').replace('\n', '').split(',')
        if len(bonus) == 1:
            script_function.append(script_json[bonus[0].lower()][0])
        else:
            script_function.append((script_json[bonus[0].lower()][0], bonus[1]))

    if 'skill' in dict_script:
        skill = dict_script['skill'][1:-4]
        skill_lvl = dict_script['skill'][-2:-1]
        script_function.append(('Enable skill', skill, skill_lvl))

    if 'bonus3' in dict_script:
        bonus3 = dict_script['bonus3'].replace(';', '').replace('\n', '').split(',')
        bonus3_name = script_json[bonus3[0].lower()][0]
        script_function.append((bonus3_name, bonus3[1], bonus3[2], bonus3[3]))

    if 'bonus_extra' in dict_script:
        for w in dict_script['bonus_extra']:
            bonus_extra = w.split(',')
            bonus_extra = [s.replace(';', '') for s in bonus_extra]
            if len(bonus_extra) != 1:
                if len(bonus_extra) != 2:
                    sufix = script_json[bonus_extra[0].lower()][0]
                    value = bonus_extra[-1].replace(';', '')
                    script_function.append((sufix, bonus_extra[1], value))
                else:
                    sufix = script_json[bonus_extra[0].lower()][0]
                    value = bonus_extra[-1]
                    script_function.append((sufix, bonus_extra[1]))
            else:
                script_function.append(script_json[bonus_extra[0].lower()][0])

    if 'bonus2_extra' in dict_script:
        for w in dict_script['bonus2_extra']:
            bonus2_extra = w.split(',')
            sufix = script_json[bonus2_extra[0].lower()][0]
            value = bonus2_extra[2].replace(';', '')
            script_function.append((sufix, bonus2_extra[1], value))

    if 'bonus3_extra' in dict_script:
        for w in dict_script['bonus3_extra']:
            bonus3_extra = w.split(',')
            if len(bonus3_extra) != 1:
                sufix = script_json[bonus3_extra[0].lower()][0]
                value = bonus3_extra[-1].replace(';', '')
                script_function.append((sufix, bonus3_extra[1], value))
            else:
                script_function.append(script_json[bonus3_extra[0].lower()][0][0])

    return script_function


def multiple_if_else_cards() -> List[int]:
    if_else_bank = []
    for i in card_db:
        c_script = card_db[i]['Script'].replace("\n", "")
        if c_script.count("if") > 1:
            if_else_bank.append(card_db[i]['Id'])
    return if_else_bank


def if_else_cards() -> List[int]:
    if_else_bank = []
    for i in card_db:
        c_script = card_db[i]['Script'].replace("\n", "")
        if c_script.count("if") == 1:
            if_else_bank.append(card_db[i]['Id'])
    return if_else_bank


for q in if_else_cards():
    name = card_db[q]['Name']
    script = card_db[q]['Script']
    analysis = analyse_single_script(script)
    print(name.replace("\n", ""))
    print(script.replace("\n", ""))
    print(analysis)
    print('')

