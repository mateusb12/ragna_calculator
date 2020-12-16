import pandas as pd
from typing import List
import os

# df = pd.read_csv('../resources/stat_points_table.csv')

csv_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'stat_points_table.csv'))
df = pd.read_csv(csv_location)


# print("caminho atual = {}".format(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))))

def attribute_balance(input_level: int, input_attribute: List[int]) -> int:
    attribute_pool = df['points'][input_level]
    total_cost = 0
    for i in input_attribute:
        total_cost += df['single_cost'][i]
    return attribute_pool - total_cost
