import pandas as pd
import os


def dynamic_choose(s1="esponja"):
    return s1


def test_function(s=None):
    dir_path = str(os.path.dirname(os.path.realpath(__file__)) + "\max_hp_table.csv")
    # print("diretório é {}".format(dir_path))
    return list(pd.read_csv(dir_path).columns)
