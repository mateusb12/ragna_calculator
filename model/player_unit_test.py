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
         BuildNuances(9195, 726, 60, 16, 151, 108, 1, 2, 1.8))

test2 = (PlayerBuild(jbl, 99, 50, 'crusader', [9, 1, 99, 1, 99, 1]).export_build(),
         BuildNuances(12724, 508, 84, 7, 201, 102, 1, 3, 2.2))

test3 = (PlayerBuild(jbl, 99, 50, 'dancer', [30, 10, 91, 99, 1, 1]).export_build(),
         BuildNuances(7868, 1232, 57, 30, 105, 116, 1, 4, 2.8))


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
