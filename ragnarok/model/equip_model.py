from ragnarok.main.exporter import db_package, equip_db, job70


class PlayerGear:
    def __init__(self, package: dict, job: str, base_level: int):
        self.armor = '(No Armor)'
        self.weapon = '(No weapon)'
        self.shield = '(No shield)'
        self.robe = '(No robe)'
        self.shoes = '(No shoes)'
        self.accessory1 = '(No accessory1)'
        self.accessory2 = '(No accessory2)'
        self.tophat = '(No tophat)'
        self.midhat = '(No midhat)'
        self.lowhat = '(No lowhat)'
        self.weapon_db = package[0]
        self.hat_db = package[1]
        self.shield_db = package[2]
        self.robe_db = package[3]
        self.armor_db = package[4]
        self.shoes_db = package[5]
        self.accessory_db = package[6]
        self.full_db = package[7]
        self.job = job
        self.base_level = base_level
        if job in job70:
            self.is_transclass = True
        else:
            self.is_transclass = False

    def equip(self, gear: dict):
        gear_id = gear['Id']
        if gear in self.armor_db.values():
            self.armor = gear
        if gear in self.shield_db.values():
            self.shield = gear
        if gear in self.robe_db.values():
            self.robe = gear
        if gear in self.shoes_db.values():
            self.shoes = gear
        if gear in self.accessory_db.values():
            if type(self.accessory2) == dict:
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

        print("Equipando {}".format(gear_id))

    def print_gear(self):
        if type(self.tophat) == dict:
            print('[Cabeça Topo] → {}'.format(self.print_single_gear(self.tophat)))
        if type(self.midhat) == dict:
            print('[Cabeça Meio] → {}'.format(self.print_single_gear(self.midhat)))
        if type(self.lowhat) == dict:
            print('[Cabeça Baixo] → {}'.format(self.print_single_gear(self.lowhat)))

        if type(self.armor) == dict:
            print('[Armadura] → {}'.format(self.print_single_gear(self.armor)))
        if type(self.weapon) == dict:
            print('[Mão direita] → {}'.format(self.print_single_gear(self.weapon)))
        else:
            print("[Mão direita] → Nothing")
        if type(self.shield == dict):
            print('[Mão esquerda] → {}'.format(self.print_single_gear(self.shield)))
        if type(self.robe == dict):
            print('[Capa] → {}'.format(self.print_single_gear(self.robe)))
        if type(self.shoes == dict):
            print('[Sapatos] → {}'.format(self.print_single_gear(self.shoes)))
        if type(self.accessory1) == dict:
            print('[Acessório] → {}'.format(self.print_single_gear(self.accessory1)))
        if type(self.accessory2) == dict:
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


pe = PlayerGear(db_package, 'champion', 94)

gear_queue = {'robe': (2504, 5),
              'shoes': (2407, 7),
              'shield': (2102, 7),
              'armor': (2322, 7),
              'acessory1': (2626, 0),
              'acessory2': (2607, 0),
              }

hat_queue = [5353, 2269]

for i, j in gear_queue.items():
    pe.equip(equip_db[j[0]])
    pe.refine_single_gear(i, j[1])

for i in hat_queue:
    pe.equip(equip_db[i])

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

# print("")
# print("")
#
# # 1471
# for i, j in equip_db[1185].items():
#     print(i, j)
#
# print(pe.is_equipable(1185))
