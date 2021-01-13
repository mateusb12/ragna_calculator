import os
import pandas as pd
from typing import List

from ragnarok.main.gear_query import dict_name_to_dict_id, is_equipable, unnest_list
from ragnarok.main.exporter import equip_db, job70, shield_db, shoes_db, armor_db, robe_db, accessory_db, \
    hat_db, weapon_db, adjective_list, job_adapt, card_db

from ragnarok.model.dead_gear import dead_gear_list as nullgear
from ragnarok.model.dead_gear import dead_card as nullcard

from itertools import chain


# nullcard = 4700
# nullgear = [2139, 2393, 2447, 2511, 2709, 5432, 5433, 5435]


class BaseGear:
    def __init__(self, gd: dict):
        self.nullcard = 4700
        self.nullgear = [2139, 2393, 2447, 2511, 2709, 5432, 5433, 5435]
        self.gear_type = ""
        self.class_type = ""
        self.id = gd['Id']
        self.aegisname = gd['AegisName']
        self.name = gd['Name']
        self.type = gd['Type']
        if 'Buy' in gd:
            self.buying_price = gd['Buy']
        else:
            self.buying_price = 40
        self.defense = 0
        if 'Defense' in gd:
            self.defense = gd['Defense']
        self.gender = None
        if 'Gender' in gd:
            self.gender = gd['Gender']
        self.locations = gd['Locations']
        self.script = gd['Script']
        if 'Script_adapted' in gd:
            self.script_adapted = gd['Script_adapted']
        self.weight = gd['Weight']
        self.slots = gd['Slots']
        self.jobs = gd['Jobs']
        self.classes = None
        if 'Classes' in gd:
            self.classes = gd['Classes']
        self.levelmin = gd['EquipLevelMin']
        self.is_refineable = gd['Refineable']
        if 'Refineable' not in gd:
            self.is_refineable = False
        self.refining = 0
        self.card = None
        self.card2 = None
        self.card3 = None
        self.card4 = None

    def __str__(self):
        str_base = "[{}] → ".format(self.class_type)
        if self.refining != 0 and self.refining is not None:
            str_base += "+{} ".format(self.refining)
        str_base += "{}".format(self.name)
        if self.slots != 0:
            str_base += " [{}]".format(self.slots)
        if self.card:
            str_base += " {}".format(self.card['Name'])
        if self.card2:
            str_base += ", {}".format(self.card2['Name'])
        if self.card3:
            str_base += ", {}".format(self.card3['Name'])
        if self.card4:
            str_base += " {}".format(self.card4['Name'])
        return str_base

    def export_text(self) -> str:
        str_base = ""
        if int(self.refining) != 0:
            str_base += "+{} ".format(self.refining)
        if self.card:
            str_base += "{} ".format(adjective_list[self.card['Id']])
        str_base += self.name
        return str_base

    def export_info(self) -> dict:
        if self.card:
            return {'id': self.id, 'refine': int(self.refining), 'card': self.card['Id'],
                    'name': self.name, 'defense': int(self.defense)}
        else:
            return {'id': self.id, 'refine': int(self.refining), 'card': "4700",
                    'name': self.name, 'defense': int(self.defense)}

    def is_dead_gear(self):
        if self.id in nullgear:
            return True
        else:
            return False

    def refine(self, amount: int) -> bool:
        if not self.is_refineable and amount is not None:
            if int(amount) != 0:
                if self.id not in self.nullgear:
                    pass
                    # raise Exception('Impossible to refine to +{} '
                    #                 'The equipment [{}] {} is not refineable'.format(amount, self.id, self.name))
        else:
            self.refining = amount
            return True

    def insert_card(self, card_id: int):
        from ragnarok.main.exporter import card_db
        if card_id == 0:
            return False
        card = card_db[card_id]
        if self.slots == 0:
            if card['Id'] != self.nullcard and self.id not in self.nullgear:
                pass
                # raise Exception('Impossible to insert card. '
                #                 'The equipment [{}] {} has zero slots'.format(self.id, self.name))
        if type(self.gear_type) is not list:
            type_check = self.gear_type.lower()
            if type_check in ['right_accessory', 'left_accessory']:
                type_check = 'both_accessory'
            if type_check not in list(card["Locations"].keys())[0].lower():
                if (card['Id'] != self.nullcard) and self.id not in self.nullgear:
                    raise Exception('Impossible to insert card. '
                                    '[{}] cannot be inserted into a [{}] ("{}"). Required: {}. Found: {}'
                                    .format(card['Name'], self.class_type, self.name,
                                            list(card["Locations"].keys())[0], self.gear_type.lower()))
        else:
            card_positions = list(card["Locations"].keys())
            equip_positions = list(self.locations.keys())
            has_intersection = bool(set(card_positions) & set(equip_positions))
            if not has_intersection:
                if card['Id'] != self.nullcard:
                    raise Exception('Impossible to insert card. '
                                    '[{}] cannot be inserted into a [{}] ("{}"). Required: {}'
                                    .format(card['Name'], self.class_type, self.name,
                                            list(card["Locations"].keys())[0]))

        self.card = card


class Shield(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in shield_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Shield'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "left_hand"
        self.class_type = "Shield"


class Shoes(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in shoes_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Shoes'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "shoes"
        self.class_type = "Shoes"


class Armor(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in armor_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Armor'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "armor"
        self.class_type = "Armor"


class Robe(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in robe_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "Garment"
        self.class_type = "Robe"


class Accessory(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in accessory_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "right_accessory"
        self.class_type = "Accessory"


class Headgear(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in hat_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = ["Head_Top", "Head_Mid", "Head_Low"]
        self.class_type = "Headgear"

    def get_hat_priority(self):
        if len(self.locations) == 1:
            return 1
        if len(self.locations) == 2:
            return 2
        if len(self.locations) == 3:
            return 3


class Weapon(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in weapon_db and gd['Id'] not in nullgear:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "right_hand"
        self.class_type = "Weapon"
        self.subtype = gd['SubType']
        self.subtype_list = ("2hSword", "2hSpear", "2hAxe", "2hStaff", "Katar", "Huuma", "Bow", "Revolver",
                             "Rifle", "Shotgun", "Gatling", "Grenade")
        self.two_handed = self.subtype in self.subtype_list

    def remaining_slots(self):
        cardlist = []
        if self.card:
            cardlist.append(True)
        if self.card2:
            cardlist.append(True)
        if self.card3:
            cardlist.append(True)
        if self.card4:
            cardlist.append(True)
        return self.slots - len(cardlist)

    def insert_card(self, card_id: int):
        from ragnarok.main.exporter import card_db
        if card_id == 0:
            return False
        card = card_db[card_id]
        if (self.slots == 0) and (self.id != 1599) and (card_id != 4700):
            raise Exception('Impossible to insert the card {}. '
                            'The weapon [{}] {} has zero slots'.format(card['Name'], self.id, self.name))
        else:
            if card_id != 4700:
                if self.card:
                    if self.card2:
                        if self.card3:
                            if self.card4:
                                raise Exception("Impossible to insert [{}] ({})."
                                                " The weapon [{}] has already {}/{} cards"
                                                .format(card['Name'], card['Id'], self.name, self.slots, self.slots))
                            else:
                                if self.remaining_slots() > 0:
                                    self.card4 = card
                                else:
                                    raise Exception("Impossible to insert [{}] ({})."
                                                    " The weapon [{}] has already {}/{} cards"
                                                    .format(card['Name'], card['Id'], self.name, self.slots,
                                                            self.slots))
                        else:
                            if self.remaining_slots() > 0:
                                self.card3 = card
                            else:
                                raise Exception("Impossible to insert [{}] ({})."
                                                " The weapon [{}] has already {}/{} cards"
                                                .format(card['Name'], card['Id'], self.name, self.slots, self.slots))
                    else:
                        if self.remaining_slots() > 0:
                            self.card2 = card
                        else:
                            raise Exception("Impossible to insert [{}] ({})."
                                            " The weapon [{}] has already {}/{} cards"
                                            .format(card['Name'], card['Id'], self.name, self.slots, self.slots))
                else:
                    self.card = card


class PlayerGear:
    def __init__(self, gear_input: dict, job: str, base_level: int):
        self.gear_input: dict
        self.job = job
        self.base_level = base_level
        self.headtop = None
        self.headmid = None
        self.headlow = None
        self.weapon = None
        self.shield = None
        self.shoes = None
        self.armor = None
        self.robe = None
        self.accessory1 = None
        self.accessory2 = None

        if self.job.lower() == 'super_novice':
            self.job = 'SuperNovice'

        if self.job.lower() == "swordsman":
            self.job = "swordman"

        self.gt = self.create_gear_table(gear_input)
        for w in self.gt:
            if not isinstance(w, Headgear):
                self.equip_item(w)

        priority_ids = {'headtop': self.gt[0].id,
                        'headmid': self.gt[1].id,
                        'headlow': self.gt[2].id}

        id_refine_card = {self.gt[0].id: (self.gt[0].refining, self.gt[0].card),
                          self.gt[1].id: (self.gt[1].refining, self.gt[1].card),
                          self.gt[2].id: (self.gt[2].refining, self.gt[2].card)}

        priority_dict = {'headtop': self.gt[0].get_hat_priority(),
                         'headmid': self.gt[1].get_hat_priority(),
                         'headlow': self.gt[2].get_hat_priority()}

        priority_podium = sorted(priority_dict, key=priority_dict.get)
        priority_queue = [priority_ids[priority_podium[0]],
                          priority_ids[priority_podium[1]],
                          priority_ids[priority_podium[2]]]

        for h in priority_queue:
            aux_head = Headgear(equip_db[h])
            aux_head.refine(id_refine_card[h][0])
            if id_refine_card[h][1] is not None:
                aux_head.insert_card(id_refine_card[h][1]['Id'])
            self.equip_item(aux_head)

        self.gear_summary = {'headtop': self.headtop, 'headmid': self.headmid, 'headlow': self.headlow,
                             'weapon': self.weapon, 'shield': self.shield, 'shoes': self.shoes,
                             'armor': self.armor, 'robe': self.robe, 'accessory1': self.accessory1,
                             'accessory2': self.accessory2, }

    def equip_item(self, item: BaseGear):
        equipable = self.is_equipable(item)
        if not equipable[0]:
            raise Exception("{}".format(equipable[1]))

        if isinstance(item, Shield):
            self.shield = item
        if isinstance(item, Shoes):
            self.shoes = item
        if isinstance(item, Armor):
            self.armor = item
        if isinstance(item, Robe):
            self.robe = item
        if isinstance(item, Accessory):
            if self.accessory1 is not None:
                self.accessory2 = item
            else:
                self.accessory1 = item
        if isinstance(item, Headgear):
            if item.locations == {'Head_Low': True}:
                self.headlow = item
            if item.locations == {'Head_Mid': True}:
                self.headmid = item
            if item.locations == {'Head_Top': True}:
                self.headtop = item
            if item.locations == {'Head_Mid': True, 'Head_Top': True}:
                self.headtop = item
                self.headmid = item
            if item.locations == {'Head_Mid': True, 'Head_Low': True}:
                self.headmid = item
                self.headlow = item
            if item.locations == {'Head_Low': True, 'Head_Mid': True, 'Head_Top': True}:
                self.headlow = item
                self.headmid = item
                self.headtop = item
        if isinstance(item, Weapon):
            self.weapon = item
            if item.two_handed:
                self.shield = Shield(equip_db[2139])

    def is_equipable(self, item: BaseGear):
        if item:
            if 'Upper' in item.classes.keys():
                if self.job.lower() not in job70:
                    return False, 'Cannot equip the transclass-only item [{}] ({}) in a {}' \
                        .format(item.name, item.id, self.job)
            current_job = self.job.lower()
            original_job = self.job.lower()
            if current_job in job70:
                current_job = job_adapt['Body'][current_job.lower()]
            if 'All' in item.jobs.keys():
                if current_job in map(lambda x: x.lower(), item.jobs.keys()):
                    return False, 'Cannot equip the item [{}] ({}) in a {}' \
                        .format(item.name, item.id, self.job)
            else:
                if current_job in ['bard', 'dancer']:
                    current_job = 'barddancer'
                if item.gender:
                    if item.gender == 'Female' and original_job == 'bard':
                        return False, 'Cannot equip the item [{}] ({}) in a {}' \
                            .format(item.name, item.id, self.job.capitalize())
                    if item.gender == 'Male' and original_job == 'dancer':
                        return False, 'Cannot equip the item [{}] ({}) in a {}' \
                            .format(item.name, item.id, self.job.capitalize())

                if current_job not in map(lambda x: x.lower(), item.jobs.keys()):
                    return False, 'Cannot equip the item [{}] ({}) in a {}' \
                        .format(item.name, item.id, self.job.capitalize())
        return True, 'equipable'

    def print_gear(self):
        print(self.headtop)
        print(self.headmid)
        print(self.headlow)
        print(self.weapon)
        print(self.shield)
        print(self.shoes)
        print(self.armor)
        print(self.robe)
        print(self.accessory1)
        print(self.accessory2)

    def unequip_noble_hats(self):
        if self.headtop:
            hat_a = self.headtop.get_hat_priority()
        else:
            hat_a = 1
        if self.headmid:
            hat_b = self.headmid.get_hat_priority()
        else:
            hat_b = 1
        if self.headlow:
            hat_c = self.headlow.get_hat_priority()
        else:
            hat_c = 1
        noble_list = [hat_a, hat_b, hat_c]

        if noble_list[0] > 1:
            self.headtop = Headgear(equip_db[5432])
        if noble_list[1] > 1:
            self.headmid = Headgear(equip_db[5433])
        if noble_list[2] > 1:
            self.headlow = Headgear(equip_db[5435])

    def has_noble_hats(self):
        if self.headtop:
            hat_a = self.headtop.get_hat_priority()
        else:
            hat_a = 1
        if self.headmid:
            hat_b = self.headmid.get_hat_priority()
        else:
            hat_b = 1
        if self.headlow:
            hat_c = self.headlow.get_hat_priority()
        else:
            hat_c = 1

        if max([hat_a, hat_b, hat_c]) == 1:
            return False
        else:
            return True

    def return_hat_dict_names(self):
        out_dict = dict()
        if self.headtop:
            out_dict['headtop'] = self.headtop.name
        else:
            out_dict['headtop'] = Headgear(equip_db[5432]).name

        if self.headmid:
            out_dict['headmid'] = self.headmid.name
        else:
            out_dict['headmid'] = Headgear(equip_db[5433]).name

        if self.headlow:
            out_dict['headlow'] = self.headlow.name
        else:
            out_dict['headlow'] = Headgear(equip_db[5435]).name
        return out_dict

    @staticmethod
    def create_gear_table(input_dict: dict) -> List[BaseGear]:
        gear_table = []
        for k, v in input_dict.items():
            aux = None
            if v is not None:
                if k == "shield" and v is not None:
                    aux = Shield(equip_db[v[0]])
                if k == "weapon" and v is not None:
                    aux = Weapon(equip_db[v[0]])
                    if len(v) > 2:
                        aux.insert_card(v[2])
                    if len(v) > 3:
                        aux.insert_card(v[3])
                    if len(v) > 4:
                        aux.insert_card(v[4])
                    if len(v) > 5:
                        aux.insert_card(v[5])
                if k == "shoes" and v is not None:
                    aux = Shoes(equip_db[v[0]])
                if k == "armor" and v is not None:
                    aux = Armor(equip_db[v[0]])
                if k == "robe" and v is not None:
                    aux = Robe(equip_db[v[0]])
                if k in ["accessory1", "accessory2"] and v is not None:
                    aux = Accessory(equip_db[v[0]])
                if k in ["headgear1", "headgear2", "headgear3"] and v is not None:
                    aux = Headgear(equip_db[v[0]])
                aux.refine(v[1])
                if k is not 'weapon':
                    aux.insert_card(v[2])
            gear_table.append(aux)
        return gear_table

    def export_id_table(self) -> dict:
        id_dict = dict()
        if self.headtop:
            id_dict['headtop'] = self.headtop.id
        else:
            id_dict['headtop'] = None
        if self.headmid:
            id_dict['headmid'] = self.headmid.id
        else:
            id_dict['headmid'] = None
        if self.headlow:
            id_dict['headlow'] = self.headlow.id
        else:
            id_dict['headlow'] = None
        if self.armor:
            id_dict['armor'] = self.armor.id
        else:
            id_dict['armor'] = None
        if self.weapon:
            id_dict['weapon'] = self.weapon.id
        else:
            id_dict['weapon'] = None
        if self.shield:
            id_dict['shield'] = self.shield.id
        else:
            id_dict['shield'] = None
        if self.robe:
            id_dict['robe'] = self.robe.id
        else:
            id_dict['robe'] = None
        if self.shoes:
            id_dict['shoes'] = self.shoes.id
        else:
            id_dict['shoes'] = None
        if self.accessory1:
            id_dict['accessory1'] = self.accessory1.id
        else:
            id_dict['accessory1'] = None
        if self.accessory2:
            id_dict['accessory2'] = self.accessory2.id
        else:
            id_dict['accessory2'] = None
        return id_dict

    def total_defense(self):
        def_sum = 0
        refine_criteria = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 6, 9: 6, 10: 7}
        for i in self.gear_summary:
            aux = self.gear_summary[i]
            if not isinstance(aux, Weapon):
                aux_info = self.gear_summary[i].export_info()
                def_sum += aux_info['defense']
                def_sum += refine_criteria[aux_info['refine']]
        return def_sum

    def script_summary(self):
        script_dict = dict()
        flat_script = []
        for g in self.gear_summary:
            aux = self.gear_summary[g]
            if aux.card == None:
                aux.card = card_db[4700]
            if not isinstance(aux, Weapon):
                if aux.class_type not in script_dict:
                    script_dict[aux.class_type] = {'Gear': (aux.name, aux.script_adapted),
                                                   'Card': (aux.card['Name'], aux.card['Script_adapted'])}
                else:
                    if "{}2".format(aux.class_type) not in script_dict:
                        script_dict["{}2".format(aux.class_type)] = {'Gear': (aux.name, aux.script_adapted),
                                                                     'Card': (aux.card['Name'], aux.card['Script_adapted'])}
                    else:
                        script_dict["{}3".format(aux.class_type)] = {'Gear': (aux.name, aux.script_adapted),
                                                                     'Card': (aux.card['Name'], aux.card['Script_adapted'])}
                flat_script.append(aux.script_adapted)
                flat_script.append(aux.card['Script_adapted'])
            else:
                wcs = {"card1": "", "card2": "", "card3": "", "card4": ""}
                if aux.card:
                    wcs["card1"] = (aux.card['Name'], aux.card['Script_adapted'])
                if aux.card2:
                    wcs["card2"] = (aux.card2['Name'], aux.card2['Script_adapted'])
                if aux.card3:
                    wcs["card3"] = (aux.card3['Name'], aux.card3['Script_adapted'])
                if aux.card4:
                    wcs["card4"] = (aux.card4['Name'], aux.card4['Script_adapted'])
                script_dict['Weapon'] = {"Gear": (aux.name, aux.script_adapted), "Card": wcs}
                flat_script.append(aux.script_adapted)
                flat_script.append(aux.card['Script_adapted'])
        flat_script = [a for a in flat_script if a != "No Script"]
        flat_script = unnest_list(flat_script)
        script_dict['Flat_list'] = flat_script
        return script_dict


def analyse_script(script_dict: dict):
    weapon_script = script_dict['Weapon']['Gear'][1]
    # accessory1_script = script_dict['Accessory']['Card'][1]
    # print(analyse_single_script(accessory1_script))


text_dict = {"headgear1": ("Valkyrie Feather Band [1]", "4", "Elder Willow Card"),
             "headgear2": ("Red Glasses", 0, "(No Card)"),
             "headgear3": ('Rainbow Scarf', 0, "(No Card)"),
             "shield": ('Guard [1]', '7', "Ambernite Card"),
             "shoes": ('Sandals [1]', '4', "Zombie Card"),
             "armor": ("Formal Suit [1]", "7", "Dokebi Card"),
             "robe": ("Muffler [1]", "7", "Raydric Card"),
             "accessory1": ("Glove [1]", 0, "Mantis Card"),
             'accessory2': ("Earring [1]", 0, "Zerom Card"),
             'weapon': ("Grimtooth", 0, "(No Card)", "(No Card)", "(No Card)", "(No Card)")}

# Muramash

gear_dict = dict_name_to_dict_id(text_dict)
pe = PlayerGear(gear_dict, 'hunter', 99)
pe.print_gear()
print('')

ttk = pe.script_summary()
for i in ttk:
    print(i, ttk[i])
print('')

for w in ttk['Flat_list']:
    print(w)

# for p in range(4001, 4500):
#     if p in card_db:
#         script = card_db[p]['Script']
#         name = card_db[p]['Name']
#         if script != 0:
#             print('item: {}'.format(p))
#             p_script = script
#             p_analysis = analyse_single_script(card_db[p]['Script'])
#             print('name = {}'.format(name))
#             print('script: {}analysis: {}'.format(p_script, p_analysis))
#             print('')


# # pe.equip_item(pe.create_item_with_id(2104))
# pe.unequip_noble_hats()
# pe.print_gear()

# print(pe.priority_queue)
# print(pe.export_id_table().values())

# print(list(pe.export_id_table().values()))

# print(pe.weapon.export_text())

