import pandas as pd
from typing import List

df = pd.read_csv('../resources/stat_points_table.csv')


def attribute_balance(input_level: int, input_attribute: List[int]) -> int:
    attribute_pool = df['points'][input_level]
    total_cost = 0
    for i in input_attribute:
        total_cost += df['single_cost'][i]
    return attribute_pool - total_cost


print(attribute_balance(99, [86, 71, 46, 17, 23, 45]))
