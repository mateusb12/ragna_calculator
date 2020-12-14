class DbGenerator:
    def __init__(self, equip_list):
        equip_main_dict = equip_list['Body']['Body2']
        equip_database = dict()
            
        for i in range(len(equip_main_dict)):
            equip_database[equip_main_dict[i]['Id']] = equip_main_dict[i]
                
        self.equip_database = equip_database
        
        print("Database carregado com sucesso!")

    @staticmethod
    def normalize_missing_params(input_db: dict) -> dict:
        copy_db = input_db
        checklist = {'Id': 0, 'Name': '', 'Weight': 0, 'Defense': 0, 'Slots': 0, 'Jobs': {'All': True},
                     'Classes': {'All': True}, 'Gender': 'Both', 'Locations': 'None', 'EquipLevelMin': 0,
                     'Refineable': False, 'View': 0, 'Script': 0, 'Refining': 0}
        for i in checklist.keys():
            if i not in input_db:
                copy_db[i] = checklist[i]
        return copy_db

    @staticmethod
    def normalize_weapon_params(input_db: dict) -> dict:
        copy_db = input_db
        checklist = {'Id': 0, 'Name': '', 'Type': 'Undefined', 'SubType': 'Undefined', 'Weight': 0, 'Attack': 0,
                     'Range': 0, 'Slots': 0, 'Jobs': {'All': True}, 'Classes': {'All': True}, 'Gender': 'Both',
                     'Locations': 'None', 'WeaponLevel': 0, 'EquipLevelMin': 0, 'Refineable': False, 'View': 0,
                     'Script': 0, 'Refining': 0}
        for i in checklist.keys():
            if i not in input_db:
                copy_db[i] = checklist[i]
        return copy_db
    
    def get_equip_db(self) -> dict:
        return self.equip_database
    
    def get_shield_db(self) -> dict:
        shield_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i and 'Type' in i:
                if i['Locations'] == {'Left_Hand': True} and i['Type'] == 'Armor':
                    shield_database[i['Id']] = self.normalize_missing_params(i)
        return shield_database
    
    def get_robe_db(self) -> dict:
        robe_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                if i['Locations'] == {'Garment': True}:
                    robe_database[i['Id']] = self.normalize_missing_params(i)
        return robe_database
                    
    def get_shoes_db(self) -> dict:
        shoes_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                if i['Locations'] == {'Shoes': True}:
                    shoes_database[i['Id']] = self.normalize_missing_params(i)
        return shoes_database
    
    def get_accessory_db(self) -> dict:
        accessory_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                if i['Locations'] == {'Right_Accessory': True, 'Left_Accessory': True}:
                    accessory_database[i['Id']] = self.normalize_missing_params(i)
        return accessory_database
    
    def get_armor_db(self) -> dict:
        armor_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                if i['Locations'] == {'Armor': True}:
                    armor_database[i['Id']] = self.normalize_missing_params(i)
        return armor_database
    
    def get_hat_db(self) -> dict:
        hat_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                combinations = ({'Head_Top': True}, {'Head_Mid': True}, {'Head_Low': True},
                                {'Head_Mid': True, 'Head_Top': True}, {'Head_Low': True, 'Head_Mid': True},
                                {'Head_Low': True, 'Head_Mid': True, 'Head_Top': True})
                if i['Locations'] in combinations:
                    hat_database[i['Id']] = self.normalize_missing_params(i)
        return hat_database
    
    def get_weapon_db(self) -> dict:
        weapon_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if 'Locations' in i:
                if i['Type'] == 'Weapon':
                    weapon_database[i['Id']] = self.normalize_weapon_params(i)
        return weapon_database
