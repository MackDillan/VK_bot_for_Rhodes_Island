from vk_api.longpoll import VkLongPoll, VkEventType
import traceback
import vk_api
import random
import time
from codecs import open

import uuid 
from peewee import *
import sqlite3

db = SqliteDatabase('Aarknights_DB.db')

class Resourse(Model):
    UID = UUIDField(primary_key=True,null=False)
    Name = CharField(max_length = 20)
    Recipe = UUIDField(null = True, default='Null')
    LVL = CharField(max_length = 1)

    class Meta:
        database = db 
        
class List_of_res(Model):
    UID = UUIDField(primary_key=True,null=False)
    Res_1 = ForeignKeyField(Resourse, field = 'UID')
    Amount_1 = IntegerField()
    Res_2 = ForeignKeyField(Resourse, field = 'UID', null = True)
    Amount_2 = IntegerField(null = True)
    Res_3 = ForeignKeyField(Resourse, field = 'UID', null = True)
    Amount_3 = IntegerField(null = True)

    class Meta:
        database = db 

class Drop_place(Model):
    UID = UUIDField(primary_key=True,null=False)
    Name = CharField(max_length = 10)
    Res = ForeignKeyField(Resourse, field = 'UID')
    Sanity_cost = IntegerField()
    
    class Meta:
        database = db 

class Recipe(Model):
    UID = UUIDField(primary_key=True,null=False)
    Resourses = ForeignKeyField(List_of_res, field = 'UID')
    class Meta:
        database = db 

class Operator(Model):
    UID = UUIDField(primary_key=True,null=False)
    Name = CharField(max_length=20)
    class Meta:
        database = db 

class Skill(Model):
    UID = UUIDField(primary_key=True,null=False)
    Name = CharField(max_length=20)
    LVL = IntegerField(constraints = [Check('LVL in (1,2,3,4,5,6,7,8,9,10)')])
    Resourses = ForeignKeyField(List_of_res, field = 'UID')
    Operator = ForeignKeyField(Operator, field = 'UID')
    Skill_number = IntegerField(constraints = [Check('Skill_number in (1,2,3)')])
    
    class Meta:
        database = db 

class Promotion(Model):
    UID = UUIDField(primary_key=True,null=False)
    LVL = IntegerField(constraints = [Check('LVL in (1,2)')])
    Resourses = ForeignKeyField(List_of_res, field = 'UID')
    Operator = ForeignKeyField(Operator, field = 'UID')
    Cost = IntegerField()

    class Meta:
        database = db 

class Amiya_bot():
    def __init__(self):
        self.vk_session = vk_api.VkApi(
            token='32319c102c6f7a48f705c4697eb8c886ce62986248f5a15eb9c702a742296a7cedbcb7c53327860707d68')

        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()
        self.mastering_dict = {
            'M1' : 8,
            'M2' : 9,
            'M3' : 10,
        }

    def send_msg(self, event, user_id, message):
        random_id = random.randint(1000000, 9999999)
        if event.from_user:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id
            )

    def hallo(self, event):
        self.send_msg(event, event.user_id,
                    'Я тут, Доктор.')

    def calc(self, event):
        self.send_msg(event, event.user_id,
                    'https://aceship.github.io/AN-EN-Tags/aklevel.html')

    def get_promotion(self, data, event):
        prom_number = False
        if data[-1].isdigit():
            data, prom_number = data[:-2], data[-1:]
        
        data = data[::-1]
        data = data.split(maxsplit=1)
        oper_name = data[1][::-1]
        if not prom_number:
            out = Promotion.select(Promotion.LVL, Promotion.Cost, Promotion.Resourses).where(Promotion.Operator == Operator.get(Operator.Name == oper_name)).dicts().execute()
        
        else:
            out = Promotion.select(Promotion.LVL, Promotion.Cost, Promotion.Resourses).where(Promotion.Operator == Operator.get(Operator.Name == oper_name), Promotion.LVL == int(prom_number)).dicts().execute()

        data ='Operator: ' + str(oper_name) + '\n\n'


        for prom in out:
            data += 'Promotion LVL: {0}\nCost: {1} LMD\n'.format(prom['LVL'], prom['Cost'])
            data += 'Resourses:\n'
            for res_list in List_of_res.select(\
                List_of_res.Res_1, List_of_res.Amount_1,\
                List_of_res.Res_2, List_of_res.Amount_2,\
                List_of_res.Res_3, List_of_res.Amount_3)\
                .where(List_of_res.UID == prom['Resourses']).dicts().execute():
                
                for i in range(1,4):
                    resours = Resourse.select(Resourse.Name).where(Resourse.UID == res_list['Res_%s'%i]).dicts().execute()
                    
                    for res in resours:
                        data += 'Resourse name: {0}\nAmount: {1}'.format(res['Name'],res_list['Amount_%s'%i])
                        data += '\n'
            
                data += '\n\n'
        
        self.send_msg(event, event.user_id,data)

    def get_skills(self, data, event):
        data = data[::-1]
        data = data.split(maxsplit=1)
        oper_name = data[1][::-1]
        out = Skill.select(Skill.Name, Skill.LVL, Skill.Resourses).where(Skill.Operator == Operator.get(Operator.Name == oper_name)).group_by(Skill.Name, Skill.LVL).dicts().execute()
       
        data ='Operator: ' + str(oper_name) + '\n\n'
        for skill in out:
            data +='Skill name: '
            data += skill['Name']
            data += '\nlvl: '
            data += str(skill['LVL'])
            data += '\nResourses:'

            for res_list in List_of_res.select(\
                List_of_res.Res_1, List_of_res.Amount_1,\
                List_of_res.Res_2, List_of_res.Amount_2,\
                List_of_res.Res_3, List_of_res.Amount_3)\
                .where(List_of_res.UID == skill['Resourses']).dicts().execute():
                for i in range(1,4):
                    resours = Resourse.select(Resourse.Name).where(Resourse.UID == res_list['Res_%s'%i]).dicts().execute()
                    for res in resours:
                        data += 'Resourse name: {0}\nAmount: {1}'.format(res['Name'],res_list['Amount_%s'%i])
                        data += '\n'
            
                data += '\n\n'
        
        self.send_msg(event, event.user_id,data)
 
    def get_skill(self, data, event):    
        data = data.split(' S')
        oper_name, skill_info = data
        try:
            skill_number, skill_lvl = skill_info.split()
        except ValueError:
            skill_number = skill_info[0]
            skill_lvl = '1-10'
        
        start_n = 0
        if 'M' in skill_lvl:
            start_n = 7
            skill_lvl = skill_lvl.replace('M','')

        if '-' in skill_lvl:
            skill_lvl = skill_lvl.split('-')
            skill_lvl = list(map(int, skill_lvl))
            skill_lvl = range(start_n+skill_lvl[0], start_n+ skill_lvl[1]+1)
        
        else:
            skill_lvl = str(int(skill_lvl)+start_n)
            skill_lvl = list(map(int, skill_lvl))
            
        out = Skill.select(Skill.Name, Skill.LVL, Skill.Resourses).where(Skill.Operator == Operator.get(Operator.Name == oper_name),\
            Skill.Skill_number == skill_number, Skill.LVL << skill_lvl).group_by(Skill.Name, Skill.LVL).dicts().execute()
            
        data ='Operator: ' + str(oper_name) + '\n\n'
        for skill in out:
            data +='Skill name: '
            data += skill['Name']
            data += '\nlvl: '
            data += str(skill['LVL'])
            data += '\nResourses:'

            for res_list in List_of_res.select(\
                List_of_res.Res_1, List_of_res.Amount_1,\
                List_of_res.Res_2, List_of_res.Amount_2,\
                List_of_res.Res_3, List_of_res.Amount_3)\
                .where(List_of_res.UID == skill['Resourses']).dicts().execute():
                for i in range(1,4):
                    resours = Resourse.select(Resourse.Name).where(Resourse.UID == res_list['Res_%s'%i]).dicts().execute()
                    for res in resours:
                        data += 'Resourse name: {0}\nAmount: {1}'.format(res['Name'],res_list['Amount_%s'%i])
                        data += '\n'
            
                data += '\n\n'
        
        self.send_msg(event, event.user_id,data)   

    def resourse(self, data, event):
        res_name = data[4:]
        
        data = 'Resourse name: %s\n\n'%res_name
        place = Drop_place.select(Drop_place.Name, Drop_place.Sanity_cost).where(Drop_place.Res == Resourse.get(Resourse.Name==res_name)).dicts().execute()

        data += 'Drop places:\n' 
        for plc in place:
            data += '{0}, Sanity cost: {1}\n'.format(plc['Name'],plc['Sanity_cost'])

        rec_uid = Resourse.get(Resourse.Name ==  res_name).Recipe
        list_of_res_uid = Recipe.select(Recipe.Resourses).where(Recipe.UID == rec_uid)
            
        for res_list in List_of_res.select(\
                List_of_res.Res_1, List_of_res.Amount_1,\
                List_of_res.Res_2, List_of_res.Amount_2,\
                List_of_res.Res_3, List_of_res.Amount_3)\
                .where(List_of_res.UID == list_of_res_uid).dicts().execute():
            
            data += "\nCraft recipe:\n"
            for i in range(1,4):
                if res_list['Res_%s'%i] != None:
                    data += "{0} {1}\n".format(Resourse.get(Resourse.UID == res_list['Res_%s'%i]).Name, res_list['Amount_%s'%i])

        self.send_msg(event, event.user_id,data)  


    def main(self):
        try:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    
                    input_data = event.text

                    if 'promotion' in input_data:
                        self.get_promotion(event.text, event)

                    elif 'skills' in input_data:
                        self.get_skills(event.text, event)
                    
                    elif 'res ' in input_data:
                        self.resourse(event.text, event)

                    elif ' S' in input_data:
                        self.get_skill(event.text, event)

                    else:
                        self.send_msg(event, event.user_id, "Команда не распознана.")




            time.sleep(2)

        except Exception as e:
            self.vk.messages.send(
                user_id=134474352,
                message=e,
                random_id=random.randint(1000000, 9999999)
            )

Resourse.create_table()
Drop_place.create_table()
Recipe.create_table()
List_of_res.create_table()
Promotion.create_table()
Skill.create_table()
Operator.create_table()

bot = Amiya_bot()
bot.main()
