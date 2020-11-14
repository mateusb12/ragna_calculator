class db_generator:
    def __init__(self):
        import yaml
        import math
        import pandas as pd
        
        with open(r'C:\Pythonfundamentos\Remember\calculadora\item_db_equip.yml') as file:
            equip_list = yaml.load(file, Loader=yaml.FullLoader)
            equip_main_dict = equip_list['Body']
            equip_database = dict()
            
            for i in range(len(equip_main_dict)):
                equip_database[equip_main_dict[i]['Id']] = equip_main_dict[i]
                
        self.equip_database = equip_database
        
        print("Database carregado com sucesso!")
        
    def normalize_missing_params(self, input_db):
        copy_db = input_db
        checklist = {'Id': 0, 'Name': '', 'Weight': 0, 'Defense': 0, 'Slots': 0, 'Jobs': {'All': True}, 'Classes': {'All': True}, 'Gender': 'Both', 'Locations': 'None', 'EquipLevelMin': 0, 'Refineable': False, 'View': 0, 'Script': 0}
        for i in checklist.keys():
            if(i not in input_db):
                copy_db[i] = checklist[i]
        return copy_db
    
    def getEquip_DB(self):
        return self.equip_database
    
    def getShield_DB(self):
        shield_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i and 'Type' in i):
                if(i['Locations'] == {'Left_Hand': True} and i['Type'] == 'Armor'):
                    shield_database[i['Id']] = self.normalize_missing_params(i)
        return shield_database
    
    def getRobe_DB(self):
        robe_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i):
                if(i['Locations'] == {'Garment': True}):
                    robe_database[i['Id']] = self.normalize_missing_params(i)
        return robe_database
                    
    def getShoes_DB(self):
        shoes_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i):
                if(i['Locations'] == {'Shoes': True}):
                    shoes_database[i['Id']] = self.normalize_missing_params(i)
        return shoes_database
    
    def getAcessory_DB(self):
        acessory_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i):
                if(i['Locations'] == {'Right_Accessory': True, 'Left_Accessory': True}):
                    acessory_database[i['Id']] = self.normalize_missing_params(i)
        return acessory_database
    
    def getArmor_DB(self):
        armor_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i):
                if(i['Locations'] == {'Armor': True}):
                    armor_database[i['Id']] = self.normalize_missing_params(i)
        return armor_database
    
    def getHat_DB(self):
        hat_database = {}
        equip_database = self.equip_database
        for i in equip_database.values():
            if('Locations' in i):
                if(((('Head_Top' or 'Head_Mid') or 'Head_Low') in i['Locations']) == True):
                    hat_database[i['Id']] = self.normalize_missing_params(i)
        return hat_database