from email import message_from_file

from button import sender
from main_code import offset, bot, line
from vk_api.longpoll import VkLongPoll, VkEventType
from DB import create_db


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        if request == 'начать поиск':
            create_db()
            bot.write_msg(user_id, f'Привет, {bot.name(user_id)}')
            bot.find_user(user_id)
            bot.write_msg(event.user_id, f'Нашёл для тебя пару, жми на кнопку "Вперёд"')


        elif request == 'вперёд':
            for i in line:
                offset += 1
                bot.write_msg(event.user_id, f'работает!??!?))))')
                break

        else:
            bot.write_msg(event.user_id, 'Твоё сообщение непонятно. Нажми на кнопку "Начать поиск", и начнём искать')