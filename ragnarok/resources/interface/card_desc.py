import os
import time
from typing import List

from bs4 import BeautifulSoup
import pandas as pd

from urllib.request import Request, urlopen
import re


def get_adjective_by_id(card_id: int):
    site = "http://db.irowiki.org/olddb/item-info/{}/".format(card_id)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")

    div_list = soup.findAll("td", {"class": "bgLtRow1 padded infoText"})
    return div_list[2].text


def generate_csv(first_list: List[int], second_list: List[str], csv_file: str):
    # csv_file = "card_adjectives.csv"
    csv_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'interface', 'adjectives', csv_file)))
    df = pd.DataFrame({'card_id': first_list, 'adjective': second_list})
    df.to_csv(csv_path, index=False)


def run_scanner():
    start_time = time.time()
    id_list = []
    adjective_list = []

    for i in range(4001, 4453):
        print('Tentando pegar {}'.format(i))
        id_list.append(i)
        adjective_list.append(str(get_adjective_by_id(i)))

    print("\n\n")
    full_time = time.time() - start_time
    if full_time < 1:
        full_time *= 1000
        print("--- {} ms ---".format(round(full_time, 4)))
    else:
        print("--- {} seconds ---".format(full_time))

    generate_csv(id_list, adjective_list, 'card_adjectives.csv')


def pandas_to_dict(input_dict: pd.DataFrame) -> dict:
    new_dict = dict()
    for q in zip(input_dict['card_id'], input_dict['adjective']):
        new_dict[q[0]] = q[1]
    return new_dict
