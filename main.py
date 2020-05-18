from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import vk_api
import random
import time
def main():
    try:
        vk_session = vk_api.VkApi(token='32319c102c6f7a48f705c4697eb8c886ce62986248f5a15eb9c702a742296a7cedbcb7c53327860707d68')

        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.text == 'Амия, калькулятор':
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Доктор, держи\nhttps://aceship.github.io/AN-EN-Tags/aklevel.html',
                            random_id = random.randint(1000000,9999999)
                        )
        time.sleep(2)
    except Exception as e:
        print(e)
        main()


main()
