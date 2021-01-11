from typing import Tuple, List

from ragnarok.model.dead_gear import dead_gear_list as nullgear
from ragnarok.model.dead_gear import dead_card as nullcard
from ragnarok.main.exporter import hat_db, weapon_db, shield_db, shoes_db, armor_db, robe_db, \
    accessory_db, \
    equip_db, card_db, job70, job_adapt


def is_equipable(player_job: str, player_level: int, ch: dict):
    current_job = player_job.lower()
    if current_job == 'super_novice':
        current_job = 'SuperNovice'
    if current_job == "swordsman":
        current_job = "Swordman"
    if 'Upper' in ch['Classes'].keys():
        if current_job not in job70:
            return False, 'Transclass only'
    if current_job in job70:
        current_job = job_adapt['Body'][current_job]

    if current_job in ['bard', 'dancer']:
        current_job = 'barddancer'

    if 'All' in ch['Jobs'].keys():
        if current_job in map(lambda x: x.lower(), ch['Jobs'].keys()):
            return False, ch['Jobs'].keys()
    else:
        if 'BardDancer' in ch['Jobs']:
            pass
        if current_job not in map(lambda x: x.lower(), ch['Jobs'].keys()):
            return False, ch['Jobs'].keys()

    if 'EquipLevelMin' in ch:
        if int(player_level) <= int(ch['EquipLevelMin']):
            return False, 'Levelmin: {}'.format(ch['EquipLevelMin'])

    return True, ch


def generate_equipable_gear(player_class: str, player_level: int) -> dict:
    equipable_headtop = set()
    equipable_headmid = set()
    equipable_headlow = set()
    equipable_weapon = set()
    equipable_shield = set()
    equipable_shoes = set()
    equipable_armor = set()
    equipable_robe = set()
    equipable_accessory = set()

    if player_class.lower() == "swordsman":
        player_class = "Swordman"
    if player_class.lower() == "super_novice":
        player_class = "SuperNovice"

    for a in hat_db:
        aux = is_equipable(player_class, player_level, hat_db[a])
        if aux[0]:
            hat_name = hat_db[a]['Name']
            if hat_db[a]['Slots'] != 0:
                hat_name += ' [1]'
            if 'Head_Top' in hat_db[a]['Locations']:
                equipable_headtop.add(hat_name)
            if 'Head_Mid' in hat_db[a]['Locations']:
                equipable_headmid.add(hat_name)
            if 'Head_Low' in hat_db[a]['Locations']:
                equipable_headlow.add(hat_name)

    for a in weapon_db:
        aux = is_equipable(player_class, player_level, weapon_db[a])
        gear_name = weapon_db[a]['Name']
        if weapon_db[a]['Slots'] != 0:
            gear_name += ' [{}]'.format(weapon_db[a]['Slots'])
        if aux[0]:
            equipable_weapon.add(gear_name)

    for a in shield_db:
        aux = is_equipable(player_class, player_level, shield_db[a])
        gear_name = shield_db[a]['Name']
        if shield_db[a]['Slots'] != 0:
            gear_name += ' [1]'
        if aux[0]:
            equipable_shield.add(gear_name)

    for a in shoes_db:
        aux = is_equipable(player_class, player_level, shoes_db[a])
        gear_name = shoes_db[a]['Name']
        if shoes_db[a]['Slots'] != 0:
            gear_name += ' [1]'
        if aux[0]:
            equipable_shoes.add(gear_name)

    for a in armor_db:
        aux = is_equipable(player_class, player_level, armor_db[a])
        gear_name = armor_db[a]['Name']
        if armor_db[a]['Slots'] != 0:
            gear_name += ' [1]'
        if aux[0]:
            equipable_armor.add(gear_name)

    for a in robe_db:
        aux = is_equipable(player_class, player_level, robe_db[a])
        gear_name = robe_db[a]['Name']
        if robe_db[a]['Slots'] != 0:
            gear_name += ' [1]'
        if aux[0]:
            equipable_robe.add(gear_name)

    for a in accessory_db:
        aux = is_equipable(player_class, player_level, accessory_db[a])
        gear_name = accessory_db[a]['Name']
        if accessory_db[a]['Slots'] != 0:
            gear_name += ' [1]'
        if aux[0]:
            equipable_accessory.add(gear_name)

    available_dict = {"headtop": list(equipable_headtop),
                      "headmid": list(equipable_headmid),
                      "headlow": list(equipable_headlow),
                      "weapon": list(equipable_weapon),
                      "shield": list(equipable_shield),
                      "shoes": list(equipable_shoes),
                      "armor": list(equipable_armor),
                      "robe": list(equipable_robe),
                      "accessory": list(equipable_accessory)}

    return available_dict


def retrieve_id_by_name(gear_name: str):
    if gear_name is not None:
        gear_tuple = adapt_slotted_name(gear_name)
        gear_name = gear_tuple[0]
        gear_slots = gear_tuple[1]
        possible_ids = []

        for j in equip_db:
            if equip_db[j]['Name'].lower() == gear_name.lower():
                if equip_db[j]['Slots'] == gear_slots:
                    return equip_db[j]['Id']
                else:
                    possible_ids.append(equip_db[j]['Id'])
        return max(possible_ids)


def retrieve_card_id_by_name(card_name: str):
    if card_name is not None:
        for d in card_db.values():
            if card_name.lower() == d['Name'].lower():
                return d['Id']
    else:
        return 4700


def adapt_slotted_name(input_name: str) -> Tuple[str, int]:
    trimmed_name = input_name
    trimmed_slots = 0
    if any(x in input_name for x in [' [1]', ' [2]', ' [3]', ' [4]']):
        trimmed_slots = int(input_name[-3:][1])
        return input_name[:-4], trimmed_slots
    else:
        return input_name, trimmed_slots


def is_refineable(gear_name: str) -> bool:
    if gear_name is not None:
        gear_name = adapt_slotted_name(gear_name)
        return equip_db[retrieve_id_by_name(gear_name[0])]['Refineable']


def has_slots(gear_name: str) -> bool:
    if gear_name is not None:
        if equip_db[retrieve_id_by_name(gear_name)]['Slots'] != 0:
            return True
        else:
            return False


def has_multiple_slots(gear_name: str) -> int:
    if gear_name is not None:
        step_aux = equip_db[retrieve_id_by_name(gear_name)]
        if step_aux['Slots'] != 0:
            return step_aux['Slots']
        else:
            return 0


def get_item_type(gear_name: str) -> str:
    ip = equip_db[retrieve_id_by_name(gear_name)]
    lc = list(ip['Locations'].keys())
    if 'Left_Hand' in lc:
        return 'shield'
    if 'Garment' in lc:
        return 'robe'
    if 'Right_Accessory' in lc:
        return 'accessory'
    if 'Armor' in lc:
        return 'armor'
    if any(i in lc for i in ['Head_Low', 'Head_Mid', 'Head_Top']):
        return 'headgear'
    if 'Right_Hand' in lc:
        return 'weapon'
    if 'Shoes' in lc:
        return 'shoes'
    return 'could not find'


def generate_equipable_cards() -> dict:
    card_dict = dict()
    card_dict['acessory_cards'] = []
    card_dict['weapon_cards'] = []
    card_dict['shield_cards'] = []
    card_dict['shoes_cards'] = []
    card_dict['robe_cards'] = []
    card_dict['armor_cards'] = []
    card_dict['headgear_cards'] = []

    for i in card_db:
        cardaux = card_db[i]['Name']
        if 'Both_Accessory' in card_db[i]['Locations']:
            card_dict['acessory_cards'].append(cardaux)
        if 'Left_Hand' in card_db[i]['Locations']:
            card_dict['shield_cards'].append(cardaux)
        if 'Head_Low' in card_db[i]['Locations']:
            card_dict['headgear_cards'].append(cardaux)
        if 'Right_Hand' in card_db[i]['Locations']:
            card_dict['weapon_cards'].append(cardaux)
        if 'Shoes' in card_db[i]['Locations']:
            card_dict['shoes_cards'].append(cardaux)
        if 'Garment' in card_db[i]['Locations']:
            card_dict['robe_cards'].append(cardaux)
        if 'Armor' in card_db[i]['Locations']:
            card_dict['armor_cards'].append(cardaux)

    return card_dict


def get_cardlist_by_name(gear_name: str):
    gear_type = get_item_type(gear_name)
    possible_cards = generate_equipable_cards()
    if gear_type == 'accessory':
        return possible_cards['acessory_cards']
    if gear_type == 'shield':
        return possible_cards['shield_cards']
    if gear_type == 'headgear':
        return possible_cards['headgear_cards']
    if gear_type == 'weapon':
        return possible_cards['weapon_cards']
    if gear_type == 'shoes':
        return possible_cards['shoes_cards']
    if gear_type == 'robe':
        return possible_cards['robe_cards']
    if gear_type == 'armor':
        return possible_cards['armor_cards']


def dict_name_to_dict_id(dict_name: dict):
    output_dict = dict_name.copy()

    for k, v in dict_name.items():
        if v is not None:
            if v[2] != 0:
                if k == 'weapon':
                    adapt_void = [retrieve_id_by_name(v[0]), v[1],
                                  retrieve_card_id_by_name(v[2]), retrieve_card_id_by_name(v[3]),
                                  retrieve_card_id_by_name(v[4]), retrieve_card_id_by_name(v[5])]
                else:
                    adapt_void = [retrieve_id_by_name(v[0]), v[1], retrieve_card_id_by_name(v[2])]
            else:
                adapt_void = [retrieve_id_by_name(v[0]), v[1], v[2]]
            output_dict[k] = adapt_void

    return output_dict


def is_id_dead_id(check_id: int) -> bool:
    if check_id in nullgear:
        return True
    else:
        return False


def has_slots_by_name(item_name: str):
    if equip_db[retrieve_id_by_name(item_name)]['Slots'] != 0:
        return True
    else:
        return False


def is_refineable_by_name(item_name: str):
    if equip_db[retrieve_id_by_name(item_name)]['Refineable']:
        return True
    else:
        return False


def normalize_form_values(pi: dict) -> dict:
    p1_gear = dict()
    headtop_t = normalize_form_values_tuple_gen('headtop', 'headgear1', pi)
    p1_gear[headtop_t['key']] = headtop_t['tuple']

    for q in [('headgear1', 'headtop'), ('headgear2', 'headmid'), ('headgear3', 'headlow'),
              ('shield', 'shield'), ('shoes', 'shoes'), ('armor', 'armor'), ('robe', 'robe'),
              ('accessory1', 'accessory1'), ('accessory2', 'accessory2'), ('weapon', 'weapon')]:
        if q[0] is not 'weapon':
            item_t = normalize_form_values_tuple_gen(q[1], q[0], pi)
            p1_gear[item_t['key']] = item_t['tuple']
        else:
            item_t = normalize_form_values_tuple_gen_for_weapon(q[1], q[0], pi)
            p1_gear[item_t['key']] = item_t['tuple']
    return p1_gear


def normalize_form_values_tuple_gen(pst: str, pst_key: str, dict_norm: dict):
    pi = dict_norm
    if ('{}_card_list'.format(pst) not in pi) or (not has_slots_by_name(pi['{}_item'.format(pst)])):
        pi['{}_card_list'.format(pst)] = '(No Card)'
    if ('{}_refine'.format(pst) not in pi) or (not is_refineable_by_name(pi['{}_item'.format(pst)])):
        pi['{}_refine'.format(pst)] = 0
    return {'tuple': (pi['{}_item'.format(pst)], pi['{}_refine'.format(pst)], pi['{}_card_list'.format(pst)]),
            'key': pst_key}


def normalize_form_values_tuple_gen_for_weapon(pst: str, pst_key: str, dict_norm: dict):
    pi = dict_norm
    if ('{}_card_1'.format(pst) not in pi) or (not has_slots_by_name(pi['{}_item'.format(pst)])):
        pi['{}_card_1'.format(pst)] = '(No Card)'
    if ('{}_card_2'.format(pst) not in pi) or (not has_slots_by_name(pi['{}_item'.format(pst)])):
        pi['{}_card_2'.format(pst)] = '(No Card)'
    if ('{}_card_3'.format(pst) not in pi) or (not has_slots_by_name(pi['{}_item'.format(pst)])):
        pi['{}_card_3'.format(pst)] = '(No Card)'
    if ('{}_card_4'.format(pst) not in pi) or (not has_slots_by_name(pi['{}_item'.format(pst)])):
        pi['{}_card_4'.format(pst)] = '(No Card)'
    if ('{}_refine'.format(pst) not in pi) or (not is_refineable_by_name(pi['{}_item'.format(pst)])):
        pi['{}_refine'.format(pst)] = 0
    return {'tuple': (pi['{}_item'.format(pst)], pi['{}_refine'.format(pst)],
                      pi['{}_card_1'.format(pst)], pi['{}_card_2'.format(pst)],
                      pi['{}_card_3'.format(pst)], pi['{}_card_4'.format(pst)]),
            'key': pst_key}


def generate_equipable_weapons_old(player_class: str, player_level: int) -> dict:
    raw_equipable_list = generate_equipable_gear(player_class, player_level)

    blank_subtype = {"Dagger": [], "1hSword": [], "2hSword": [], "1hSpear": [], "2hSpear": [],
                     "1hAxe": [], "2hAxe": [], "Mace": [], "1hStaff": [], "2hStaff": [], "Bow": [],
                     "Knuckle": [], "Musical": [], "Whip": [], "Book": [], "Katar": [], "Revolver": [],
                     "Rifle": [], "Gatling": [], "Shotgun": [], "Grenade": [], "Huuma": []}

    for a in raw_equipable_list['weapon']:
        aux = weapon_db[retrieve_id_by_name(a)]
        if aux['Slots'] != 0:
            blank_subtype[aux['SubType']].append(aux['Name'] + " [{}]".format(aux['Slots']))
        else:
            blank_subtype[aux['SubType']].append(aux['Name'])

    trimmed_blank = blank_subtype.copy()
    for b in blank_subtype:
        if not blank_subtype[b]:
            trimmed_blank.pop(b, None)
        else:
            trimmed_blank[b].sort()

    final_weapon_list = []
    final_weapon_positions = dict()

    for c in trimmed_blank.items():
        final_weapon_list.append(c[0])
        for d in c[1]:
            final_weapon_list.append(d)

    for e in range(len(final_weapon_list)):
        if final_weapon_list[e] in blank_subtype.keys():
            final_weapon_positions["weapon_item-{}".format(e)] = {"disabled": ""}

    return {'list': final_weapon_list, 'positions': final_weapon_positions}


def unnest_list(nested: List) -> List:
    nested_copy = nested.copy()
    for element in nested:
        if any(isinstance(q, list) for q in element):
            for g in element:
                nested_copy.append(g)
            nested_copy.remove(element)
    return nested_copy


def generate_equipable_weapons(player_class: str, player_level: int) -> list:
    raw_equipable_list = generate_equipable_gear(player_class, player_level)

    blank_subtype = {"Dagger": [], "1hSword": [], "2hSword": [], "1hSpear": [], "2hSpear": [],
                     "1hAxe": [], "2hAxe": [], "Mace": [], "Staff": [], "2hStaff": [], "Bow": [],
                     "Knuckle": [], "Musical": [], "Whip": [], "Book": [], "Katar": [], "Revolver": [],
                     "Rifle": [], "Gatling": [], "Shotgun": [], "Grenade": [], "Huuma": []}

    for a in raw_equipable_list['weapon']:
        aux = weapon_db[retrieve_id_by_name(a)]
        if aux['Slots'] != 0:
            blank_subtype[aux['SubType']].append(aux['Name'] + " [{}]".format(aux['Slots']))
        else:
            blank_subtype[aux['SubType']].append(aux['Name'])
        # blank_subtype[aux['SubType']].append(aux['Name'])

    trimmed_blank = blank_subtype.copy()
    for b in blank_subtype:
        if not blank_subtype[b]:
            trimmed_blank.pop(b, None)
        else:
            trimmed_blank[b].sort()

    outer_tuple = []
    for g, h in trimmed_blank.items():
        void_tuple = []
        for pkl in h:
            void_tuple.append((pkl.lower(), pkl.capitalize()))
        outer_tuple.append((g, tuple(void_tuple)))

    return list(outer_tuple)


def generate_aspd_table() -> dict:
    aspd_dict = \
        {"novice": {"Unarmed": 1, "Dagger": 1.3, "1hSword": 1.4, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": 1.6, "2hAxe": None, "1hStaff": 1.3, "2hStaff": None, "Mace": 1.4, "Bow": None,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "swordman": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1.1, "2hSword": 1.2, "1hSpear": 1.3, "2hSpear": 1.4,
                      "1hAxe": 1.4, "2hAxe": 1.5, "1hStaff": None, "2hStaff": None, "Mace": 1.3, "Bow": None,
                      "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                      "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "knight": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1, "2hSword": 1.1, "1hSpear": 1.2, "2hSpear": 1.2,
                    "1hAxe": 1.4, "2hAxe": 1.4, "1hStaff": None, "2hStaff": None, "Mace": 1.3, "Bow": None,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "crusader": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1.1, "2hSword": 1.2, "1hSpear": 1.2, "2hSpear": 1.2,
                      "1hAxe": 1.4, "2hAxe": 1.4, "1hStaff": None, "2hStaff": None, "Mace": 1.3, "Bow": None,
                      "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                      "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "magician": {"Unarmed": 1, "Dagger": 1.2, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                      "1hAxe": None, "2hAxe": None, "1hStaff": 1.4, "2hStaff": None, "Mace": None, "Bow": None,
                      "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                      "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "wizard": {"Unarmed": 1, "Dagger": 1.15, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": None, "2hAxe": None, "1hStaff": 1.25, "2hStaff": None, "Mace": None, "Bow": None,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "sage": {"Unarmed": 0.9, "Dagger": 1.05, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                  "1hAxe": None, "2hAxe": None, "1hStaff": 1.25, "2hStaff": 1.25, "Mace": None, "Bow": None,
                  "Katar": None, "Book": 1.1, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                  "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "acolyte": {"Unarmed": 0.8, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                     "1hAxe": None, "2hAxe": None, "1hStaff": 1.2, "2hStaff": None, "Mace": 1.2, "Bow": None,
                     "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                     "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "priest": {"Unarmed": 0.8, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": None, "2hAxe": None, "1hStaff": 1.2, "2hStaff": None, "Mace": 1.2, "Bow": None,
                    "Katar": None, "Book": 1.2, "Knuckle": 4, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "monk": {"Unarmed": 0.8, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                  "1hAxe": None, "2hAxe": None, "1hStaff": 1.15, "2hStaff": None, "Mace": 1.15, "Bow": None,
                  "Katar": None, "Book": None, "Knuckle": 0.95, "Musical": None, "Whip": None, "Revolver": None,
                  "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "thief": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1.3, "2hSword": None, "1hSpear": None, "2hSpear": None,
                   "1hAxe": 1.6, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": 1.6,
                   "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                   "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "assassin": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1.3, "2hSword": None, "1hSpear": None, "2hSpear": None,
                      "1hAxe": 1.6, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": None,
                      "Katar": 1, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                      "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "rogue": {"Unarmed": 0.8, "Dagger": 1, "1hSword": 1.1, "2hSword": None, "1hSpear": None, "2hSpear": None,
                   "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": None,
                   "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                   "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "merchant": {"Unarmed": 0.8, "Dagger": 1.2, "1hSword": 1.4, "2hSword": None, "1hSpear": None, "2hSpear": None,
                      "1hAxe": 1.4, "2hAxe": 1.5, "1hStaff": None, "2hStaff": None, "Mace": 1.4, "Bow": None,
                      "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                      "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "blacksmith": {"Unarmed": 0.8, "Dagger": 1.2, "1hSword": 1.3, "2hSword": None, "1hSpear": None,
                        "2hSpear": None, "1hAxe": 1.3, "2hAxe": 1.3, "1hStaff": None, "2hStaff": None, "Mace": 1.35,
                        "Bow": None, "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None,
                        "Revolver": None, "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None,
                        "Huuma": None},
         "alchemist": {"Unarmed": 0.8, "Dagger": 1.1, "1hSword": 1.15, "2hSword": None, "1hSpear": None,
                       "2hSpear": None, "1hAxe": 1.35, "2hAxe": 1.4, "1hStaff": None, "2hStaff": None, "Mace": 1.3,
                       "Bow": None, "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None,
                       "Revolver": None, "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None,
                       "Huuma": None},
         "archer": {"Unarmed": 0.8, "Dagger": 1.2, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": 1.4,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "hunter": {"Unarmed": 0.8, "Dagger": 1.15, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": 1.2,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "bard": {"Unarmed": 0.8, "Dagger": 1.1, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                  "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": 1.3,
                  "Katar": None, "Book": None, "Knuckle": None, "Musical": 1.15, "Whip": None, "Revolver": None,
                  "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "dancer": {"Unarmed": 0.8, "Dagger": 1.1, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                    "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": 1.3,
                    "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": 1.15, "Revolver": None,
                    "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "gunslinger": {"Unarmed": 1, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None,
                        "2hSpear": None, "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None,
                        "Bow": None, "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None,
                        "Revolver": 1.4, "Rifle": 1.5, "Gatling": 3, "Shotgun": 1.4, "Grenade": 3, "Huuma": None},
         "ninja": {"Unarmed": 0.8, "Dagger": 1, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                   "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": None,
                   "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                   "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": 1.5},
         "taekwon": {"Unarmed": 0.8, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None, "2hSpear": None,
                     "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None, "Mace": None, "Bow": None,
                     "Katar": None, "Book": None, "Knuckle": None, "Musical": None, "Whip": None, "Revolver": None,
                     "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None, "Huuma": None},
         "star_gladiator": {"Unarmed": 0.8, "Dagger": None, "1hSword": None, "2hSword": None, "1hSpear": None,
                            "2hSpear": None, "1hAxe": None, "2hAxe": None, "1hStaff": None, "2hStaff": None,
                            "Mace": None, "Bow": None, "Katar": None, "Book": None, "Knuckle": None, "Musical": None,
                            "Whip": None, "Revolver": None, "Rifle": None, "Gatling": None, "Shotgun": None,
                            "Grenade": None, "Huuma": None},
         "soul_linker": {"Unarmed": 1, "Dagger": 1.5, "1hSword": None, "2hSword": None, "1hSpear": None,
                         "2hSpear": None, "1hAxe": None, "2hAxe": None, "1hStaff": 1.25, "2hStaff": None, "Mace": None,
                         "Bow": None, "Katar": None, "Book": 1, "Knuckle": None, "Musical": None, "Whip": None,
                         "Revolver": None, "Rifle": None, "Gatling": None, "Shotgun": None, "Grenade": None,
                         "Huuma": None},
         "job_adapt": {"super_novice": "novice", "swordsman": "swordman", "lord_knight": "knight", "high_priest": "priest",
                       "high_wizard": "wizard", "whitesmith": "blacksmith", "sniper": "hunter",
                       "assassin_cross": "assassin", "paladin": "crusader", "stalker": "rogue", "professor": "sage",
                       "creator": "alchemist", "champion": "monk", "clown": "bard", "gypsy": "dancer"}}

    return aspd_dict


ttp = {"headtop_item": 'Ribbon', 'headlow_refine': 0, 'headlow_card_list': '(No Card)',
       "headmid_item": 'Sunglasses',
       "headlow_item": 'Romantic Flower',
       "weapon_item": 'Gladius [3]', 'weapon_refine': 7,
       'weapon_card_1': 'Assaulter Card', 'weapon_card_2': 'Assaulter Card', 'weapon_card_3': 'Andre Larva Card',
       "shield_item": 'Guard [1]', 'shield_card_list': 'Thara Frog Card',
       "shoes_item": 'Sandals',
       "armor_item": 'Silk Robe',
       "robe_item": 'Muffler',
       "accessory1_item": 'Rosary',
       "accessory2_item": 'Rosary'}

void_dict = {'headgear1': ('(No Headtop)', '0', '(No Card)'),
             'headgear2': ('(No Headmid)', 0, '(No Card)'),
             'headgear3': ('(No Headlow)', 0, '(No Card)'),
             'shield': ('(No Shield)', '0', '(No Card)'),
             'shoes': ('(No Shoes)', '0', '(No Card)'),
             'armor': ('(No Armor)', '0', 'Marc Card'),
             'robe': ('(No Robe)', '0', '(No Card)'),
             'accessory1': ('(No Accessory)', 0, '(No Card)'),
             'accessory2': ('(No Accessory)', 0, '(No Card)'),
             'weapon': ('(No Weapon)', 0, '(No Card)', '(No Card)', '(No Card)', '(No Card)')}

void_gear = dict_name_to_dict_id(void_dict)

# test1 = generate_equipable_weapons('Bard', 99)
# print(test1)

# print('')
# print('')

# print(generate_equipable_weapons("Swordsman", 99))
print(is_equipable("Swordman", 99, equip_db[1231]))
