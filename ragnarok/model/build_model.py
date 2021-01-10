import math
from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List, Optional
import os

from ragnarok.model.equip_model import PlayerGear
from ragnarok.main.gear_query import void_gear, generate_aspd_table
from ragnarok.main.gear_query import void_gear
from ragnarok.main.exporter import job70


class PlayerBuild:
    def __init__(self, job_bonuses_list: pd.DataFrame, base_level: int, job_level: int,
                 current_job: str, stat_build: List[int], playergear: Optional[PlayerGear] = void_gear):

        self.job_bonuses_list = job_bonuses_list
        self.base_level = base_level
        self.job_level = job_level
        self.current_job = current_job
        self.stat_build = stat_build
        self.str = stat_build[0]
        self.str_bonus = 0
        self.core_str = self.str
        self.agi = stat_build[1]
        self.agi_bonus = 0
        self.core_agi = self.agi
        self.vit = stat_build[2]
        self.vit_bonus = 0
        self.core_vit = self.vit
        self.int = stat_build[3]
        self.int_bonus = 0
        self.core_int = self.int
        self.dex = stat_build[4]
        self.dex_bonus = 0
        self.core_dex = self.dex
        self.luk = stat_build[5]
        self.luk_bonus = 0
        self.core_luk = self.luk
        self.cost_list = []
        self.possible_points = []
        self.playergear = playergear
        self.script_dict = playergear.script_summary()

        # arquivos
        self.hp_df = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'max_hp_table.csv')))
        self.attribute_df = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'stat_points_table.csv')))
        self.job_bonuses = self.job_bonuses_list[current_job]['FULL_BONUSES']
        self.max_job = self.job_bonuses_list[current_job]['MAX_JOB']

        # classes
        self.u_dict = self.universal_script()

        # incremento dos atributos de acordo com o nível atual de classe
        self.str_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['STR']) + self.u_dict["+str"]
        self.agi_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['AGI']) + self.u_dict["+agi"]
        self.vit_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['VIT']) + self.u_dict["+vit"]
        self.int_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['INT']) + self.u_dict["+int"]
        self.dex_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['DEX']) + self.u_dict["+dex"]
        self.luk_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['LUK']) + self.u_dict["+luk"]

        # somatórios de status
        self.str += self.str_bonus
        self.agi += self.agi_bonus
        self.vit += self.vit_bonus
        self.int += self.int_bonus
        self.dex += self.dex_bonus
        self.luk += self.luk_bonus

        # esquiva, precisão, crítico e bônus de regen
        self.flee_bonuses = self.u_dict["+flee"]
        self.perfect_dodge_bonuses = self.u_dict["+perfectdodge"]
        self.hit_bonuses = self.u_dict["+hit"]
        self.crit_bonuses = self.u_dict["+crit"]
        self.hpr_mod = self.u_dict['+hprecovery_%']
        self.spr_mod = self.u_dict['+sprecovery_%']

        # cálculo do HP
        self.trans_mod = self.job_bonuses_list[current_job]['TRANS_MOD']
        self.additive_modifiers = self.u_dict["+maxhp_flat"]
        self.multiplicative_modifiers = self.u_dict["+maxhp_%"]
        self.base_hp = list(self.hp_df[self.current_job])[self.base_level]
        self.max_hp = self.calculate_max_hp()

        # cálculo do SP
        self.sp_mod_a = self.u_dict["+maxsp_flat"]
        self.sp_mod_b = self.u_dict["+maxsp_%"]
        self.max_sp = self.calculate_max_sp()

        # esquiva
        self.flee = self.agi + self.flee_bonuses + self.base_level
        self.perfect_flee = 1 + math.floor(1 / 10 * self.luk) + self.perfect_dodge_bonuses
        self.true_perfect_flee = 1 + 1 / 10 * self.luk + self.perfect_dodge_bonuses

        # precisão
        self.hit = self.dex + self.hit_bonuses + self.base_level

        # crítico
        self.crit_rate = 1 + math.floor(1 / 3 * self.luk + self.crit_bonuses)
        self.crit_truerate = 1 + (1 / 3 * self.luk + self.crit_bonuses)
        self.crit_shield = 1 + (0.2 * self.luk)

        # hp regen
        hpr = max(1, math.floor(self.max_hp / 200))
        hpr += math.floor(self.vit / 5)
        self.hpr = math.floor(hpr * (1 + (self.hpr_mod * 0.01)))

        # sp regen
        spr = 1 + (math.floor(self.max_sp / 100))
        spr += math.floor(self.int / 6)
        if self.int >= 120:
            spr += math.floor((self.int / 2) - 56)
        self.spr = math.floor(spr * (1 + (self.spr_mod * 0.01)))

        # saldo de atributos
        attribute_cost = 0
        self.attribute_pool = self.attribute_df['points'][self.base_level]
        for i in self.stat_build:
            attribute_aux = self.attribute_df['single_cost'][i]
            attribute_cost += attribute_aux
            self.cost_list.append(attribute_aux)
        self.attribute_balance = self.attribute_pool - attribute_cost

        for i in range(len(self.cost_list)):
            big_sum = self.attribute_balance + self.attribute_df['single_cost'][i] + self.cost_list[i]
            possible_stat = self.attribute_df['single_cost'].sub(big_sum).abs().idxmin() - 1
            if possible_stat == 98:
                possible_stat += 1
            if self.attribute_balance == 0:
                possible_stat = 0
            self.possible_points.append(possible_stat)
            self.possible_points = [(x * 0 if x == y else y) for x, y in zip(self.stat_build, self.possible_points)]
            self.possible_points = [(x * 0 if x > y else y) for x, y in zip(self.stat_build, self.possible_points)]

        # ASPD
        self.aspd = self.calculate_aspd()

        # Ataque
        self.atk_base = 109
        self.atk_bonus = 0

        # Defesa
        self.def_hard = self.script_hard_defense()
        self.def_soft = math.floor(self.vit * (1 + (self.u_dict['+softdef_%'] / 100)))

        # Defesa mágica
        self.mdef_hard = self.u_dict["+mdef_flat"]
        self.mdef_soft = self.int

        # Ataque mágico
        self.matk_min = 20
        self.matk_max = 25

        print('cara? {}'.format(self.calculate_aspd()))

    def calculate_base_hp(self):
        hp_job_a = self.job_bonuses_list[self.current_job]['HP_JOB_A']
        hp_job_b = self.job_bonuses_list[self.current_job]['HP_JOB_B']
        base_hp = 35 + (self.base_level * hp_job_b)
        for i in range(2, self.base_level + 1):
            base_hp = base_hp + round(hp_job_a * i)
        return base_hp

    def calculate_max_hp(self) -> int:
        max_hp = math.floor(self.base_hp * (1 + (0.01 * self.vit)) * self.trans_mod)
        max_hp += self.additive_modifiers
        max_hp = math.floor(max_hp * (1 + (self.multiplicative_modifiers * 0.01)))
        if self.current_job in job70:
            max_hp -= 1
        return max_hp

    def calculate_max_sp(self) -> int:
        base_sp = 10
        base_sp += math.floor(self.base_level * self.job_bonuses_list[self.current_job]['SP_JOB'])
        max_sp = base_sp
        max_sp = math.floor(max_sp * (1 + (self.int * 0.01)))
        max_sp += self.sp_mod_a
        max_sp = math.floor(max_sp * (1 + (self.sp_mod_b * 0.01)))
        max_sp = math.floor(max_sp * self.trans_mod)
        return max_sp

    def script_hard_defense(self) -> int:
        hard_def = 0
        hard_def += self.playergear.total_defense()
        hard_def_a = self.u_dict['+def_flat']
        hard_def_b = self.u_dict['+def_%']

        hard_def += hard_def_a
        hard_def = math.floor(hard_def * (1 + (hard_def_b / 100)))
        return hard_def

    def universal_script(self) -> dict:
        key_list = [j[0] for j in self.script_dict['Flat_list']]
        key_list += ["+str", "+agi", "+vit", "+int", "+dex", "+luk", "+def_flat", "+def_%", "+softdef_%", "+mdef_flat",
                     "+flee", "+perfectdodge", "+hit", "+hprecovery_%", "+sprecovery_%", "+crit",
                     "+maxhp_flat", "+maxsp_flat", "+maxhp_%", "+maxsp_%"]
        key_dict = dict.fromkeys(set(key_list), 0)
        forbidden_list = ("whenhit_badstatus", "afterkill_drainsp", "resist_element_%")

        for element in self.script_dict['Flat_list']:
            if element[0] not in forbidden_list:
                key_dict[element[0]] += int(element[1])

        return key_dict

    def calculate_aspd(self) -> str:
        aspd_table = generate_aspd_table()
        adapted_job = self.current_job
        weapon_type = self.playergear.weapon.subtype
        if self.playergear.weapon.name == "(No Weapon)":
            weapon_type = "Unarmed"
        if self.current_job in [x.lower() for x in aspd_table["job_adapt"].keys()]:
            adapted_job = aspd_table["job_adapt"][self.current_job]
        aspd_bonuses = 0
        wd = 50 * aspd_table[adapted_job][weapon_type]
        aspd = 200-(wd-(((wd/25*self.agi)+(wd/100*self.dex))/10)*(1-aspd_bonuses))
        return round(aspd, 1)



    @staticmethod
    def evaluate_stat_bonus(job_level: int, stat_array: List[int]) -> int:
        global k
        if not stat_array:
            return 0
        for i in range(len(stat_array) - 1, -2, -1):
            k = i + 1
            if k == 0:
                break
            if job_level >= stat_array[i]:
                break
        return k

    def export_build(self):
        epb = BuildNuances(self.max_hp, self.max_sp, self.hpr, self.spr, self.hit,
                           self.flee, self.perfect_flee, self.crit_rate, round(self.crit_shield, 3),
                           self.str_bonus, self.agi_bonus, self.vit_bonus,
                           self.int_bonus, self.dex_bonus, self.luk_bonus,
                           self.attribute_balance, self.aspd, self.atk_base, self.atk_bonus,
                           self.def_hard, self.def_soft, self.matk_min, self.matk_max,
                           self.mdef_hard, self.mdef_soft, self.possible_points)
        return epb

    def print_build(self):
        print("Base level → {}".format(self.base_level))
        print("Job level → {}".format(self.job_level))
        print("Class → {}".format(self.current_job))
        print("")

        if self.str_bonus == 0:
            print("	[str] → {}".format(self.core_str))
        else:
            print('	[str] → {} +{}'.format(self.core_str, self.str_bonus))

        if self.agi_bonus == 0:
            print("	[agi] → {}".format(self.core_agi))
        else:
            print('	[agi] → {} +{}'.format(self.core_agi, self.agi_bonus))

        if self.vit_bonus == 0:
            print("	[vit] → {}".format(self.core_vit))
        else:
            print('	[vit] → {} +{}'.format(self.core_vit, self.vit_bonus))

        if self.int_bonus == 0:
            print("	[int] → {}".format(self.core_int))
        else:
            print('	[int] → {} +{}'.format(self.core_int, self.int_bonus))

        if self.dex_bonus == 0:
            print("	[dex] → {}".format(self.core_dex))
        else:
            print('	[dex] → {} +{}'.format(self.core_dex, self.dex_bonus))

        if self.luk_bonus == 0:
            print("	[luk] → {}".format(self.core_luk))
        else:
            print('	[luk] → {} +{}'.format(self.core_luk, self.luk_bonus))

        print("")
        print("max_hp → {}".format(self.max_hp))
        print("max_sp → {}".format(self.max_sp))
        print('hp_regen → {}'.format(self.hpr))
        print('sp_regen → {}'.format(self.spr))
        print("")
        print("hit → {}".format(self.hit))
        print("flee → {} +{}      (true_pdodge → {})".format(self.flee, self.perfect_flee, self.true_perfect_flee))
        print("critical → {}       (true_critical → {})".format(self.crit_rate, self.crit_truerate))
        print('crit_shield → {}'.format(self.crit_shield))


@dataclass
class BuildNuances:
    max_hp: int
    max_sp: int
    hp_regen: int
    sp_regen: int
    hit: int
    flee: int
    perfect_dodge: int
    critical: int
    critical_shield: float
    str_bonus: int
    agi_bonus: int
    vit_bonus: int
    int_bonus: int
    dex_bonus: int
    luk_bonus: int
    attribute_balance: int
    aspd: int
    atk_base: int
    atk_bonus: int
    def_hard: int
    def_soft: int
    matk_min: int
    matk_max: int
    mdef_hard: int
    mdef_soft: int
    possible_points: List[int]
