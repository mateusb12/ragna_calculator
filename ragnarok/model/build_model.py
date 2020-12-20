import math
from dataclasses import dataclass
import pandas as pd
from typing import List
import os


class PlayerBuild:
    def __init__(self, job_bonuses_list: pd.DataFrame, base_level: int, job_level: int,
                 current_job: str, stat_build: List[int]):

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

        # arquivos
        self.hp_df = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'max_hp_table.csv')))
        self.attribute_df = pd.read_csv(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'stat_points_table.csv')))
        self.job_bonuses = self.job_bonuses_list[current_job]['FULL_BONUSES']
        self.max_job = self.job_bonuses_list[current_job]['MAX_JOB']

        # incremento dos atributos de acordo com o nível atual de classe
        self.str_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['STR'])
        self.agi_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['AGI'])
        self.vit_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['VIT'])
        self.int_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['INT'])
        self.dex_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['DEX'])
        self.luk_bonus = self.evaluate_stat_bonus(self.job_level, self.job_bonuses_list[current_job]['LUK'])

        # somatórios de status
        self.str += self.str_bonus
        self.agi += self.agi_bonus
        self.vit += self.vit_bonus
        self.int += self.int_bonus
        self.dex += self.dex_bonus
        self.luk += self.luk_bonus

        # esquiva, precisão, crítico e bônus de regen
        self.flee_bonuses = 0
        self.hit_bonuses = 0
        self.crit_bonuses = 0
        self.hpr_mod = 0
        self.spr_mod = 0

        # cálculo do HP
        self.trans_mod = self.job_bonuses_list[current_job]['TRANS_MOD']
        self.additive_modifiers = 0
        self.multiplicative_modifiers = 0
        self.base_hp = list(self.hp_df[self.current_job])[self.base_level]
        self.max_hp = self.calculate_max_hp()

        # cálculo do SP
        self.sp_mod_a = 0
        self.sp_mod_b = 0
        self.max_sp = self.calculate_max_sp()

        # esquiva
        self.flee = self.agi + self.flee_bonuses + self.base_level
        self.perfect_dodge_bonuses = 0
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
        attribute_pool = self.attribute_df['points'][self.base_level]
        for i in self.stat_build:
            attribute_cost += self.attribute_df['single_cost'][i]
        self.attribute_balance = attribute_pool - attribute_cost

        # ASPD
        self.aspd = 172

        # Ataque
        self.atk_base = 109
        self.atk_bonus = 0

        # Defesa
        self.def_hard = 22
        self.def_soft = 100

        # Ataque mágico
        self.matk_min = 20
        self.matk_max = 25

        # Defesa mágica
        self.mdef_hard = 2
        self.mdef_soft = 5

    def calculate_base_hp(self):
        hp_job_a = self.job_bonuses_list[self.current_job]['HP_JOB_A']
        hp_job_b = self.job_bonuses_list[self.current_job]['HP_JOB_B']
        base_hp = 35 + (self.base_level * hp_job_b)
        for i in range(2, self.base_level + 1):
            base_hp = base_hp + round(hp_job_a * i)
        return base_hp

    def calculate_max_hp(self) -> int:
        max_hp = math.floor(self.base_hp * (1 + (0.01 * self.vit)))
        max_hp += self.additive_modifiers
        max_hp = math.floor(max_hp * (1 + (self.multiplicative_modifiers * 0.01)))
        return max_hp

    def calculate_max_sp(self) -> int:
        base_sp = 10
        base_sp += math.floor(self.base_level * self.job_bonuses_list[self.current_job]['SP_JOB'])
        max_sp = base_sp
        max_sp = math.floor(max_sp * (1 + (self.int * 0.01)))
        max_sp += self.sp_mod_a
        max_sp = math.floor(max_sp * (1 + (self.sp_mod_b * 0.01)))
        return max_sp

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
                           self.mdef_hard, self.mdef_soft)
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

