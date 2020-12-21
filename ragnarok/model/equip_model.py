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

    def is_equipable(self, chosen_id: int):
        chosen_gear = self.full_db[chosen_id]
        job_restriction = chosen_gear['Jobs']
        level_restriction = chosen_gear['EquipLevelMin']
        transclass_restriction = chosen_gear['Classes']

        result = {'job': True, 'level': True, 'trans': True}

        if self.job in job_restriction:
            if job_restriction[self.job]:
                result['job'] = True
            else:
                result['job'] = False
        if self.base_level >= level_restriction:
            result['level'] = True
        else:
            result['level'] = False

        for i in result.values():
            if not i:
                return False, result
        return True, result


from ragnarok.main.exporter import db_package, equip_db

pe = PlayerGear(db_package, 'monk', 44)
pe.equip(equip_db[2504])
pe.refine_single_gear('robe', 5)

pe.equip(equip_db[2407])
pe.refine_single_gear('shoes', 7)

pe.equip(equip_db[2102])
pe.refine_single_gear('shield', 7)

pe.equip(equip_db[2322])
pe.refine_single_gear('armor', 7)

pe.equip(equip_db[5353])  # sun god
pe.equip(equip_db[2269])  # romantic flower
pe.equip(equip_db[2626])  # rosary
pe.equip(equip_db[2607])  # clip

pe.equip(equip_db[1471])

print("")
pe.print_gear()
print("")
print("")

for i, j in equip_db[1471].items():
    print(i, j)

print(pe.is_equipable(1471))
