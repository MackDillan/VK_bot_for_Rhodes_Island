from vk_api.longpoll import VkLongPoll, VkEventType
#import requests
import vk_api
import random
import time
from codecs import open
class Amiya_bot():
        
    def __init__(self):
        self.vk_session = vk_api.VkApi(
            token='32319c102c6f7a48f705c4697eb8c886ce62986248f5a15eb9c702a742296a7cedbcb7c53327860707d68')

        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()

    def get_id_for_msg(self):
        return random.randint(1000000, 9999999)

    def send_msg(self, event, user_id, message):
        random_id = random.randint(1000000, 9999999)
        if event.from_user:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id
            )

    def main(self):
        try:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    if event.text == 'Амия, калькулятор':
                        self.send_msg(event,event.user_id,
                                'Доктор, держи\nhttps://aceship.github.io/AN-EN-Tags/aklevel.html')

                    elif event.text.startswith('Добавь ссылку'):
                        text = event.text.split('ссылку')[1]
                        text = text.split('http')
                        url = 'http'+text[1]
                        try:
                            out = open('urls.txt', 'ab', 'utf-8')

                        except FileNotFoundError:
                            out = open('urls.txt', 'wb', 'utf-8')

                        out.write('{0}   {1}\n'.format(text[0], url))
                        out.close()

                        self.send_msg(event,event.user_id,
                                "Доктор, я добавила ссылку в архив.")
            
                    elif event.text.startswith('Дай архив'):
                        data = str()

                        try:
                            with open('urls.txt', 'r', encoding="utf-8") as fl:
                                itr = 1
                                for line in fl:
                                    data += "{0} {1} \n".format(itr, line)
                                    itr += 1

                        except FileNotFoundError:
                            pass

                        if not data:
                            data = 'База пуста'

                        self.send_msg(event,event.user_id, data)

                    elif event.text.startswith('Обнови запись в архиве номер '):
                        data = list()
                        try:
                            with open('urls.txt', 'rb', encoding="utf-8") as fl:
                                for line in fl:
                                    data.append(line)
                                    
                            text = event.text
                            text_split = text[len(
                                'Обнови запись в архиве номер '):][0]

                            nmbr = int(text_split[0])
                            
                            text_split = text[text.find(' описание '):].replace(
                                ' описание ', '').replace(' ссылка', '').split(' ', 1)

                            data[nmbr-1] = '{0}   {1}\n'.format(text_split[0], text_split[1])
                            out = open('urls.txt', 'wb', 'utf-8')

                            for i in data:
                                out.write(i)
                            out.close()

                        except FileNotFoundError:
                            pass

                        if not data:
                            data = 'База пуста'

                        self.send_msg(event,event.user_id, 'Архив обновлён')
            
            time.sleep(2)

        except Exception as e:
            self.vk.messages.send(
                user_id=134474352,
                message=e,
                random_id=random.randint(1000000, 9999999)
            )

bot = Amiya_bot()
bot.main()
