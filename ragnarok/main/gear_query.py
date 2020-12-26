from ragnarok.main.exporter import hat_db, is_equipable, weapon_db, shield_db, shoes_db, armor_db, robe_db, \
    accessory_db, \
    equip_db, card_db


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
            gear_name += ' [1]'
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
        original_name = gear_name
        gear_name = adapt_slotted_name(gear_name)
        plausible_ids = dict()
        for k in equip_db.values():
            if k['Name'].lower() == gear_name.lower():
                plausible_ids[k['Id']] = k['Slots']
        if ' [1]' in original_name:
            return max(plausible_ids, key=plausible_ids.get)
        else:
            # mudar para minimo
            return min(plausible_ids, key=plausible_ids.get)


def retrieve_card_id_by_name(card_name: str):
    for d in card_db.values():
        if card_name.lower() == d['Name'].lower():
            return d['Id']


def adapt_slotted_name(input_name: str) -> str:
    if ' [1]' in input_name:
        return input_name[:-4]
    else:
        return input_name


def is_refineable(gear_name: str) -> bool:
    if gear_name is not None:
        gear_name = adapt_slotted_name(gear_name)
        return equip_db[retrieve_id_by_name(gear_name)]['Refineable']


def has_slots(gear_name: str) -> bool:
    if gear_name is not None:
        if equip_db[retrieve_id_by_name(gear_name)]['Slots'] != 0:
            return True
        else:
            return False


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
                adapt_void = [retrieve_id_by_name(v[0]), v[1], retrieve_card_id_by_name(v[2])]
            else:
                adapt_void = [retrieve_id_by_name(v[0]), v[1], v[2]]
            output_dict[k] = adapt_void

    return output_dict

