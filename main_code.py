from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import config
import database
from database import *
from config import *

vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)
session_api = vk.get_api()

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            id = event.user_id
            config.user_id_insert = id
            user_get = session_api.users.get(user_ids=(id))
            user_get = user_get[0]
            first_name = user_get['first_name']
            config.first_name_insert = first_name
            last_name = user_get['last_name']
            config.last_name_insert = last_name
            if request == "привет" or request == "Привет" or request == "Начать поиск" or request == "начать поиск":
                write_msg(event.user_id, f"Привет, {first_name}")
                database.create()
                database.insert_user()
            elif request == "Пока" or request == "пока" or request == "конец":
                write_msg(event.user_id, f"Пока. До скорых встреч, {first_name}")

            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
