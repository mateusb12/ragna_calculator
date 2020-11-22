from decorador_db_gen import DbGenerator
import yaml
import math
import pandas as pd
import logging
import os

dir_path = os.path.dirname(os.path.realpath('job_bonuses.yml'))

with open(r'{}\\job_bonuses.yml'.format(dir_path)) as file:
    job_bonuses_list = yaml.load(file, Loader=yaml.FullLoader)

dbg = DbGenerator()

equip_db = dbg.getEquip_DB()

weapon_db = dbg.getWeapon_DB()
hat_db = dbg.getHat_DB()
shield_db = dbg.getShield_DB()
robe_db = dbg.getRobe_DB()
armor_db = dbg.getArmor_DB()
shoes_db = dbg.getShoes_DB()
acessory_db = dbg.getAcessory_DB()

db_package = (weapon_db, hat_db, shield_db, robe_db, armor_db, shoes_db, acessory_db)
