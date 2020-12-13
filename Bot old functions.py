    #old functions
        # def add_link(self, event):
        #     text = event.text.split('ссылку')[1]
        #     text = text.split('http')
        #     url = 'http'+text[1]
        #     try:
        #         out = open('urls.txt', 'ab', 'utf-8')

        #     except FileNotFoundError:
        #         out = open('urls.txt', 'wb', 'utf-8')

        #     out.write('{0}   {1}\n'.format(text[0], url))
        #     out.close()

        #     self.send_msg(event, event.user_id,
        #         "Доктор, я добавила ссылку в архив.")

        # def get_archive(self, event):
        #     data = str()

        #     try:
        #         with open('urls.txt', 'r', encoding="utf-8") as fl:
        #             itr = 1
        #             for line in fl:
        #                 data += "{0} {1} \n".format(itr, line)
        #                 itr += 1

        #     except FileNotFoundError:
        #         pass

        #     if not data:
        #         data = 'База пуста'

        #     self.send_msg(event, event.user_id, data)

        # def update_line(self, event):
        #     data = list()
        #     try:
        #         with open('urls.txt', 'rb', encoding="utf-8") as fl:
        #             for line in fl:
        #                 data.append(line)

        #         text = event.text
        #         text_split = text[len(
        #             'Обнови запись номер '):][0]

        #         nmbr = int(text_split[0])

        #         text_split = text[text.find(' описание '):].replace(
        #             ' описание ', '').replace(' ссылка', '').split(' ', 1)

        #         data[nmbr-1] = '{0}   {1}\n'.format(
        #             text_split[0], text_split[1])
        #         out = open('urls.txt', 'wb', 'utf-8')

        #         for i in data:
        #             out.write(i)
        #         out.close()

        #     except FileNotFoundError:
        #         pass

        #     if not data:
        #         data = 'База пуста'

        #     self.send_msg(event, event.user_id, 'Архив обновлён')

        # def del_line(self, event):
        #     data = list()
        #     try:
        #         with open('urls.txt', 'rb', encoding="utf-8") as fl:
        #             for line in fl:
        #                 data.append(line)

        #         text = event.text

        #         text_split = text[len(
        #             'Удали запись номер '):]

        #         nmbr = int(text_split)-1

        #         data.remove(data[nmbr])
        #         out = open('urls.txt', 'wb', 'utf-8')

        #         for i in data:
        #             out.write(i)
        #         out.close()

        #     except FileNotFoundError:
        #         pass

        #     if not data:
        #         data = 'База пуста'

        #     self.send_msg(event, event.user_id, 'Архив обновлён')