from model.build_model import PlayerBuild
from model.build_model import BuildNuances
import os
import pandas as pd
import time

start_time = time.time()


def open_json(filename):
    folder_name = 'resources'
    dir_path = (os.path.dirname(os.path.realpath(filename))[:-5] + '\\{}\\'.format(folder_name)) + filename
    return pd.read_json(r'{}'.format(dir_path))


jbl = open_json('job_bonuses.json')

test1 = (PlayerBuild(jbl, 99, 50, 'monk', [89, 2, 73, 51, 48, 1]).export_build(),
         BuildNuances(9195, 726, 60, 16, 151, 108, 1, 2, 1.8, 8, 7, 6, 2, 4, 3, 1,
                      172, 109, 0, 22, 100, 20, 25))

test2 = (PlayerBuild(jbl, 99, 50, 'crusader', [9, 1, 99, 1, 99, 1]).export_build(),
         BuildNuances(12724, 508, 84, 7, 201, 102, 1, 3, 2.2, 7, 2, 7, 6, 3, 5, 1,
                      172, 109, 0, 22, 100, 20, 25))

test3 = (PlayerBuild(jbl, 99, 50, 'dancer', [30, 10, 91, 99, 1, 1]).export_build(),
         BuildNuances(7868, 1232, 57, 30, 105, 116, 1, 4, 2.8, 2, 7, 3, 5, 5, 8, 1,
                      172, 109, 0, 22, 100, 20, 25))


def player_test(kit):
    unit_test = kit[0]
    correct_value = kit[1]
    assert unit_test.max_hp == correct_value.max_hp
    assert unit_test.max_sp == correct_value.max_sp
    assert unit_test.hp_regen == correct_value.hp_regen
    assert unit_test.sp_regen == correct_value.sp_regen
    assert unit_test.hit == correct_value.hit
    assert unit_test.flee == correct_value.flee
    assert unit_test.perfect_dodge == correct_value.perfect_dodge
    assert unit_test.critical == correct_value.critical
    assert unit_test.critical_shield == correct_value.critical_shield
    assert unit_test.str_bonus == correct_value.str_bonus
    assert unit_test.agi_bonus == correct_value.agi_bonus
    assert unit_test.vit_bonus == correct_value.vit_bonus
    assert unit_test.int_bonus == correct_value.int_bonus
    assert unit_test.dex_bonus == correct_value.dex_bonus
    assert unit_test.luk_bonus == correct_value.luk_bonus
    assert unit_test.attribute_balance == correct_value.attribute_balance
    assert unit_test.aspd == correct_value.aspd
    assert unit_test.atk_base == correct_value.atk_base
    assert unit_test.atk_bonus == correct_value.atk_bonus
    assert unit_test.def_hard == correct_value.def_hard
    assert unit_test.def_soft == correct_value.def_soft
    assert unit_test.matk_min == correct_value.matk_min
    assert unit_test.matk_max == correct_value.matk_max


player_test(test1)
player_test(test2)
player_test(test3)

full_time = time.time() - start_time
if full_time < 1:
    full_time *= 1000
    print("--- {} ms ---".format(round(full_time, 4)))
else:
    print("--- {} seconds ---".format(full_time))
print("Working normally.")
