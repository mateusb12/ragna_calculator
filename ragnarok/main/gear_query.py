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
            if 'Head_Top' in hat_db[a]['Locations']:
                equipable_headtop.add(hat_db[a]['Name'])
            if 'Head_Mid' in hat_db[a]['Locations']:
                equipable_headmid.add(hat_db[a]['Name'])
            if 'Head_Low' in hat_db[a]['Locations']:
                equipable_headlow.add(hat_db[a]['Name'])

    for a in weapon_db:
        aux = is_equipable(player_class, player_level, weapon_db[a])
        if aux[0]:
            equipable_weapon.add(weapon_db[a]['Name'])

    for a in shield_db:
        aux = is_equipable(player_class, player_level, shield_db[a])
        if aux[0]:
            equipable_shield.add(shield_db[a]['Name'])

    for a in shoes_db:
        aux = is_equipable(player_class, player_level, shoes_db[a])
        if aux[0]:
            equipable_shoes.add(shoes_db[a]['Name'])

    for a in armor_db:
        aux = is_equipable(player_class, player_level, armor_db[a])
        if aux[0]:
            equipable_armor.add(armor_db[a]['Name'])

    for a in robe_db:
        aux = is_equipable(player_class, player_level, robe_db[a])
        if aux[0]:
            equipable_robe.add(robe_db[a]['Name'])

    for a in accessory_db:
        aux = is_equipable(player_class, player_level, accessory_db[a])
        if aux[0]:
            equipable_accessory.add(accessory_db[a]['Name'])

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
        plausible_ids = dict()
        for k in equip_db.values():
            if k['Name'].lower() == gear_name.lower():
                plausible_ids[k['Id']] = k['Slots']
        return max(plausible_ids, key=plausible_ids.get)


def is_refineable(gear_name: str) -> bool:
    if gear_name is not None:
        return equip_db[retrieve_id_by_name(gear_name)]['Refineable']


def has_slots(gear_name: str) -> bool:
    if gear_name is not None:
        if equip_db[retrieve_id_by_name(gear_name)]['Slots'] != 0:
            return True
        else:
            return False


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
        if 'Both_Accessory' in card_db[i]['Locations']:
            card_dict['acessory_cards'].append(card_db[i])
        if 'Left_Hand' in card_db[i]['Locations']:
            card_dict['shield_cards'].append(card_db[i])
        if 'Head_Low' in card_db[i]['Locations']:
            card_dict['headgear_cards'].append(card_db[i])
        if 'Right_Hand' in card_db[i]['Locations']:
            card_dict['weapon_cards'].append(card_db[i])
        if 'Shoes' in card_db[i]['Locations']:
            card_dict['shoes_cards'].append(card_db[i])
        if 'Garment' in card_db[i]['Locations']:
            card_dict['robe_cards'].append(card_db[i])
        if 'Armor' in card_db[i]['Locations']:
            card_dict['armor_cards'].append(card_db[i])

    return card_dict


print(generate_equipable_cards()['shield_cards'])
