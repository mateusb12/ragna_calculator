from typing import List

from ragnarok.main.exporter import db_package, equip_db, job70, shield_db, shoes_db, armor_db, robe_db


class PlayerGear:
    def __init__(self, package: dict, job: str, base_level: int):
        self.armor = {'Type': None, 'Slots': 0}
        self.weapon = {'Type': None, 'Slots': 0}
        self.shield = {'Type': None, 'Slots': 0}
        self.robe = {'Type': None, 'Slots': 0}
        self.shoes = {'Type': None, 'Slots': 0}
        self.accessory1 = {'Type': None, 'Slots': 0}
        self.accessory2 = {'Type': None, 'Slots': 0}
        self.tophat = {'Type': None, 'Slots': 0}
        self.midhat = {'Type': None, 'Slots': 0}
        self.lowhat = {'Type': None, 'Slots': 0}
        self.weapon_db = package[0]
        self.hat_db = package[1]
        self.shield_db = package[2]
        self.robe_db = package[3]
        self.armor_db = package[4]
        self.shoes_db = package[5]
        self.accessory_db = package[6]
        self.full_db = package[7]
        self.card_db = package[8]
        self.job = job
        self.base_level = base_level
        if job in job70:
            self.is_transclass = True
        else:
            self.is_transclass = False

    def equip(self, gear: dict):
        if gear in self.armor_db.values():
            self.armor = gear
        if gear in self.shield_db.values():
            self.shield = gear
        if gear in self.robe_db.values():
            self.robe = gear
        if gear in self.shoes_db.values():
            self.shoes = gear
        if gear in self.accessory_db.values():
            if self.accessory2['Type'] is not None:
                self.accessory1 = gear
            else:
                self.accessory2 = gear
        if gear in self.weapon_db.values():
            if gear['Locations'] == {'Right_Hand': True, 'Left_Hand': True}:
                self.shield = gear
                self.weapon = gear
            if gear['Locations'] == {'Right_Hand': True}:
                self.weapon = gear
        if gear in self.hat_db.values():
            if gear['Locations'] == {'Head_Low': True}:
                self.lowhat = gear
            if gear['Locations'] == {'Head_Mid': True}:
                self.midhat = gear
            if gear['Locations'] == {'Head_Top': True}:
                self.tophat = gear
            if gear['Locations'] == {'Head_Mid': True, 'Head_Top': True}:
                self.midhat = gear
                self.tophat = gear
            if gear['Locations'] == {'Head_Mid': True, 'Head_Low': True}:
                self.midhat = gear
                self.lowhat = gear
            if gear['Locations'] == {'Head_Low': True, 'Head_Mid': True, 'Head_Top': True}:
                self.tophat = gear
                self.midhat = gear
                self.lowhat = gear

    def equip_card(self, card_id: int) -> bool:
        card = self.card_db[card_id]
        success = False
        if card_id == 0 or card_id is None:
            return success
        if len(card['Locations']) == 1:
            location = list(card['Locations'].keys())[0]
            if location.lower() == "armor" and self.armor['Slots'] != 0:
                self.armor['Card'] = card
                success = True
            if location.lower() == "shoes" and self.shoes['Slots'] != 0:
                self.shoes['Card'] = card
                success = True
            if location.lower() == "garment" and self.robe['Slots'] != 0:
                self.robe['Card'] = card
                success = True
            if location.lower() == "right_hand" and self.weapon['Slots'] != 0:
                self.weapon['Card'] = card
                success = True
            if location.lower() == "left_hand" and self.shield['Slots'] != 0:
                self.shield['Card'] = card
                success = True
            if location.lower() == "both_accessory" and self.has_accessory_slot():
                pass
        return success

    def equip_hat_card(self, card_id: int, location: str) -> bool:
        success = False
        if card_id == 0 or card_id is None:
            return success
        if self.is_top_mid_equal() and self.tophat['Slots'] != 0:
            self.tophat['Card'] = self.card_db[card_id]
            self.midhat['Card'] = self.card_db[card_id]
            success = True
        else:
            if location.lower() == 'top' and self.tophat['Slots'] != 0:
                self.tophat['Card'] = self.card_db[card_id]
                success = True
            if location.lower() == 'mid' and self.midhat['Slots'] != 0:
                self.midhat['Card'] = self.card_db[card_id]
                success = True
        return success

    def equip_ring_card(self, card_id: int, location: str) -> bool:
        success = False
        if card_id == 0 or card_id is None:
            return success
        if location.lower() == "left" and self.accessory1['Slots'] != 0:
            self.accessory1['Card'] = self.card_db[card_id]
            success = True
        if location.lower() == 'right' and self.accessory2['Slots'] != 0:
            self.accessory2['Card'] = self.card_db[card_id]
            success = True
        return success

    def print_gear(self):
        if self.tophat['Type'] is not None:
            if 'Card' in self.tophat:
                print('[Cabeça Topo] → {} [{}]'.format(self.print_single_gear(self.tophat),
                                                       self.tophat['Card']['Name']))
            else:
                print('[Cabeça Topo] → {}'.format(self.print_single_gear(self.tophat)))

        if self.midhat['Type'] is not None:
            if 'Card' in self.midhat:
                print('[Cabeça Meio] → {} [{}]'.format(self.print_single_gear(self.midhat),
                                                       self.midhat['Card']['Name']))
            else:
                print('[Cabeça Meio] → {}'.format(self.print_single_gear(self.midhat)))

        if self.lowhat['Type'] is not None:
            if 'Card' in self.lowhat:
                print('[Cabeça Baixo] → {} [{}]'.format(self.print_single_gear(self.lowhat),
                                                        self.lowhat['Card']['Name']))
            else:
                print('[Cabeça Baixo] → {}'.format(self.print_single_gear(self.lowhat)))

        if self.armor['Type'] is not None:
            if 'Card' in self.armor:
                print('[Armadura] → {} [{}]'.format(self.print_single_gear(self.armor), self.armor['Card']['Name']))
            else:
                print('[Armadura] → {}'.format(self.print_single_gear(self.armor)))

        if self.weapon['Type'] is not None:
            print('[Mão direita] → {}'.format(self.print_single_gear(self.weapon)))
        else:
            print("[Mão direita] → Nothing")

        if self.shield['Type'] is not None:
            if 'Card' in self.shield:
                print('[Mão esquerda] → {} [{}]'.format(self.print_single_gear(self.shield),
                                                        self.shield['Card']['Name']))
            else:
                print('[Mão esquerda] → {}'.format(self.print_single_gear(self.shield)))

        if self.robe['Type'] is not None:
            if 'Card' in self.robe:
                print('[Capa] → {} [{}]'.format(self.print_single_gear(self.robe), self.robe['Card']['Name']))
            else:
                print('[Capa] → {}'.format(self.print_single_gear(self.robe)))

        if self.shoes['Type'] is not None:
            if 'Card' in self.shoes:
                print('[Sapatos] → {} [{}]'.format(self.print_single_gear(self.shoes), self.shoes['Card']['Name']))
            else:
                print('[Sapatos] → {}'.format(self.print_single_gear(self.shoes)))

        if self.accessory1['Type'] is not None:
            if 'Card' in self.accessory1:
                print('[Acessório] → {} [{}]'.format(self.print_single_gear(self.accessory1),
                                                     self.accessory1['Card']['Name']))
            else:
                print('[Acessório] → {}'.format(self.print_single_gear(self.accessory1)))
        if self.accessory2['Type'] is not None:
            if 'Card' in self.accessory2:
                print('[Acessório] → {} [{}]'.format(self.print_single_gear(self.accessory2),
                                                     self.accessory2['Card']['Name']))
            else:
                print('[Acessório] → {}'.format(self.print_single_gear(self.accessory2)))

    @staticmethod
    def print_single_gear(gear) -> str:
        output_string = ''
        if 'Refining' in gear:
            if gear['Refining'] != 0:
                output_string += '+{} '.format(gear['Refining'])
        output_string += gear['Name']
        if 'Slots' in gear:
            if gear['Slots'] != 0:
                output_string += ' [{}]'.format(gear['Slots'])
        return output_string

    def refine_single_gear(self, chosen_gear: str, amount: int):
        if amount > 10 or amount < 0:
            raise ValueError('Invalid refine value +{} for {}.'.format(amount, chosen_gear))
        if amount == 0:
            pass
        if chosen_gear == 'armor':
            self.armor['Refining'] = amount
        if chosen_gear == 'shield':
            self.shield['Refining'] = amount
        if chosen_gear == 'robe':
            self.robe['Refining'] = amount
        if chosen_gear == 'shoes':
            self.shoes['Refining'] = amount
        if chosen_gear == 'weapon':
            self.weapon['Refining'] = amount

    def is_top_mid_equal(self):
        if self.tophat['Id'] == self.midhat['Id']:
            return True
        else:
            return False

    def has_accessory_slot(self):
        if self.accessory1['Slots'] != 0 or self.accessory2['Slots'] != 0:
            return True
        else:
            return False

    @staticmethod
    def adapt_class(input_class: str) -> str:
        class_table = {
            "lord_knight": "knight", "high_priest": "priest", "high_wizard": "wizard",
            "whitesmith": "blacksmith", "sniper": "hunter", "assassin_cross": "assassin",
            "paladin": "crusader", "stalker": "rogue", "professor": "sage",
            "creator": "alchemist", "champion": "monk", "clown": "bard", "gypsy": "dancer",
        }
        if input_class in class_table:
            return class_table[input_class.lower()]
        else:
            raise ValueError('[{}] is not a transclass, so it cant be adapted'.format(input_class))

    def is_equipable(self, chosen_id: int):
        chosen_gear = self.full_db[chosen_id]
        job_restriction = chosen_gear['Jobs']
        level_restriction = chosen_gear['EquipLevelMin']
        transclass_restriction = chosen_gear['Classes']
        adapted_job = self.job
        if self.is_transclass:
            adapted_job = self.adapt_class(self.job)

        result = {'job': True, 'level': True, 'trans': True}

        if 'All' not in job_restriction:
            if adapted_job not in job_restriction:
                result['job'] = False
        else:
            if adapted_job in job_restriction:
                result['job'] = False

        if self.base_level >= level_restriction:
            result['level'] = True
        else:
            result['level'] = False

        if not self.is_transclass and transclass_restriction == {'Upper': True}:
            result['trans'] = False

        for q in result.values():
            if not q:
                return False, result
        return True, result


class BaseGear:
    def __init__(self, gd: dict):
        self.gear_type = ""
        self.class_type = ""
        self.id = gd['Id']
        self.aegisname = gd['AegisName']
        self.name = gd['Name']
        self.type = gd['Type']
        self.buying_price = gd['Buy']
        self.defense = gd['Defense']
        self.locations = gd['Locations']
        self.script = gd['Script']
        self.weight = gd['Weight']
        self.slots = gd['Slots']
        self.jobs = gd['Jobs']
        self.classes = None
        if 'classes' in gd:
            self.classes = gd['classes']
        self.levelmin = gd['EquipLevelMin']
        self.is_refineable = gd['Refineable']
        if 'Refineable' not in gd:
            self.is_refineable = False
        self.refining = 0
        self.card = None

    def __str__(self):
        str_base = "[{}] → ".format(self.class_type)
        if self.refining != 0:
            str_base += "+{} ".format(self.refining)
        str_base += "{}".format(self.name)
        if self.slots != 0:
            str_base += " [{}]".format(self.slots)
        if self.card:
            str_base += " {}".format(self.card['Name'])
        return str_base

    def refine(self, amount: int) -> bool:
        if not self.is_refineable:
            raise Exception('The equipment [{}] {} is not refineable'.format(self.id, self.name))
        else:
            self.refining = amount
            return True

    def insert_card(self, card_id: int):
        from ragnarok.main.exporter import card_db
        if card_id == 0:
            return False
        card = card_db[card_id]
        if self.slots == 0:
            raise Exception('Impossible to insert card. '
                            'The equipment [{}] {} has zero slots'.format(self.id, self.name))
        if self.gear_type.lower() not in list(card["Locations"].keys())[0].lower():
            raise Exception('Impossible to insert card. '
                            '[{}] cannot be inserted into a [{}]. Required: {}'
                            .format(card['Name'], self.class_type, list(card["Locations"].keys())[0]))
        self.card = card


class Shield(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in shield_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Shield'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "left_hand"
        self.class_type = "Shield"


class Shoes(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in shoes_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Shoes'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "shoes"
        self.class_type = "Shoes"


class Armor(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in armor_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Armor'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "armor"
        self.class_type = "Armor"


class Robe(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in robe_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "Garment"
        self.class_type = "Robe"


pe = PlayerGear(db_package, 'champion', 94)

gear_dict = {"shield": (2104, 5, 4058),
             "shoes": (2407, 7, 0),
             "armor": (2322, 4, 4105),
             "robe": (2504, 5, 4133)}


def create_gear_table(input_dict: dict) -> List[BaseGear]:
    gear_table = []
    for k, v in input_dict.items():
        aux = None
        if k == "shield":
            aux = Shield(equip_db[v[0]])
        if k == "shoes":
            aux = Shoes(equip_db[v[0]])
        if k == "armor":
            aux = Armor(equip_db[v[0]])
        if k == "robe":
            aux = Robe(equip_db[v[0]])
        aux.refine(v[1])
        aux.insert_card(v[2])
        gear_table.append(aux)
    return gear_table


gear1 = create_gear_table(gear_dict)
for i in gear1:
    print(i)

# shield1 = Shield(equip_db[2104])
# shield1.refine(5)
# shield1.insert_card(4058)
# # shield1.insert_card(0)
# print(shield1)
#
# shoes1 = Shoes(equip_db[2407])
# shoes1.refine(7)
# print(shoes1)
#
# armor1 = Armor(equip_db[2322])
# armor1.refine(4)
# armor1.insert_card(4105)
# print(armor1)
#
# robe1 = Robe(equip_db[2504])
# robe1.refine(5)
# robe1.insert_card(4133)
# print(robe1)

gear_queue = {'robe': (2504, 5, 0),
              'shoes': (2407, 7, 0),
              'shield': (2102, 7, 0),
              'armor': (2322, 7, 0),
              'acessory1': (2626, 0, 0),
              'acessory2': (2607, 0, 0),
              }

hat_queue = {'hat1': 5353,
             'hat2': 2269,
             }

# Tentar validar as coisas através de classes

for i, j in gear_queue.items():
    pe.equip(equip_db[j[0]])
    pe.refine_single_gear(i, j[1])

for i in hat_queue.values():
    pe.equip(equip_db[i])

# # marc
# pe.equip_card(4105)
#
# # thara
# pe.equip_card(4058)
#
# # raydric
# pe.equip_card(4133)
#
# # salgueiro
# pe.equip_hat_card(4010, 'top')
#
# # esporo
# pe.equip_ring_card(4010, 'left')
#
# # fumacento
# pe.equip_ring_card(4044, 'right')

# pe.equip(equip_db[2504])
# pe.refine_single_gear('robe', 5)
#
# pe.equip(equip_db[2407])
# pe.refine_single_gear('shoes', 7)
#
# pe.equip(equip_db[2102])
# pe.refine_single_gear('shield', 7)
#
# pe.equip(equip_db[2322])
# pe.refine_single_gear('armor', 7)
#
# pe.equip(equip_db[5353])  # sun god
# pe.equip(equip_db[2269])  # romantic flower
# pe.equip(equip_db[2626])  # rosary
# pe.equip(equip_db[2607])  # clip
#
# pe.equip(equip_db[1471])

print("")
pe.print_gear()
print("")

# for i, j in pe.armor.items():
#     print(i, j)

# print("")
# print("")
#
# # 1471
# for i, j in equip_db[1185].items():
#     print(i, j)
#
# print(pe.is_equipable(1185))
