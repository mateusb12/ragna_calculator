from typing import List

from ragnarok.main.exporter import equip_db, job70, shield_db, shoes_db, armor_db, robe_db, accessory_db, \
    hat_db, weapon_db


class BaseGear:
    def __init__(self, gd: dict):
        self.gear_type = ""
        self.class_type = ""
        self.id = gd['Id']
        self.aegisname = gd['AegisName']
        self.name = gd['Name']
        self.type = gd['Type']
        self.buying_price = gd['Buy']
        self.defense = 0
        if 'Defense' in gd:
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
        self.card2 = None
        self.card3 = None
        self.card4 = None

    def __str__(self):
        str_base = "[{}] → ".format(self.class_type)
        if self.refining != 0:
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

    def refine(self, amount: int) -> bool:
        if not self.is_refineable:
            if amount != 0:
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
        if type(self.gear_type) is not list:
            if self.gear_type.lower() not in list(card["Locations"].keys())[0].lower():
                raise Exception('Impossible to insert card. '
                                '[{}] cannot be inserted into a [{}] ("{}"). Required: {}'
                                .format(card['Name'], self.class_type, self.name, list(card["Locations"].keys())[0]))
        else:
            card_positions = list(card["Locations"].keys())
            equip_positions = list(self.locations.keys())
            has_intersection = bool(set(card_positions) & set(equip_positions))
            if not has_intersection:
                raise Exception('Impossible to insert card. '
                                '[{}] cannot be inserted into a [{}] ("{}"). Required: {}'
                                .format(card['Name'], self.class_type, self.name, list(card["Locations"].keys())[0]))

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


class Accessory(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in accessory_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "right_accessory"
        self.class_type = "Accessory"


class Headgear(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in hat_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = ["Head_Top", "Head_Mid", "Head_Low"]
        self.class_type = "Headgear"


class Weapon(BaseGear):
    def __init__(self, gd: dict):
        if gd['Id'] not in weapon_db:
            raise Exception('INSTANTIATION ERROR. The equipment [{}] ({}) cannot be a Robe'
                            .format(gd['Name'], list(gd['Locations'].keys())[0]))
        super().__init__(gd)
        self.gear_type = "right_hand"
        self.class_type = "Weapon"

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
        if self.slots == 0:
            raise Exception('Impossible to insert card. '
                            'The equipment [{}] {} has zero slots'.format(self.id, self.name))
        else:
            if self.card:
                if self.card2:
                    if self.card3:
                        if self.card4:
                            raise Exception("Impossible to insert [{}]. The weapon [{}] has already {}/{} cards"
                                            .format(card['Name'], self.name, self.slots, self.slots))
                        else:
                            if self.remaining_slots() > 0:
                                self.card4 = card
                            else:
                                raise Exception("Impossible to insert [{}]. The weapon [{}] has already {}/{} cards"
                                                .format(card['Name'], self.name, self.slots, self.slots))
                    else:
                        if self.remaining_slots() > 0:
                            self.card3 = card
                        else:
                            raise Exception("Impossible to insert [{}]. The weapon [{}] has already {}/{} cards"
                                            .format(card['Name'], self.name, self.slots, self.slots))
                else:
                    if self.remaining_slots() > 0:
                        self.card2 = card
                    else:
                        raise Exception("Impossible to insert [{}]. The weapon [{}] has already {}/{} cards"
                                        .format(card['Name'], self.name, self.slots, self.slots))
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

        self.gt = self.create_gear_table(gear_input)
        for w in self.gt:
            self.equip_item(w)

    def equip_item(self, item: BaseGear):
        if isinstance(item, Weapon):
            self.weapon = item
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
                    for t in v[2]:
                        aux.insert_card(t)
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


gear_dict = {"headgear1": (5093, 9, 4288),
             "headgear2": None,
             "headgear3": (2269, 0, 0),
             "weapon": (1220, 7, [4035, 4035, 4092]),
             "shield": (2104, 5, 4058),
             "shoes": (2407, 7, 0),
             "armor": (2322, 4, 4105),
             "robe": (2504, 5, 4133),
             "accessory1": (2607, 0, 0),
             "accessory2": (2626, 0, 0)}

pe = PlayerGear(gear_dict, 'champion', 94)
pe.print_gear()
