import vk_api
import requests
import datetime

from config import *
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from DB import *

line = range(0, 1000)
class VKBot:
    def __init__(self):
        print('Bot was created')
        self.vk = vk_api.VkApi(token=access_token_group)
        self.longpoll = VkLongPoll(self.vk)
    def write_msg(self, user_id, message): #метод для сообщений
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


    def name(self, user_id): #Получение имени пользователя, который пишет
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                for value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена(user_token)')

    def get_sex(self, user_id):  # получение пола, и смена пола на противоположный для поиска

        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response[f'response']
            for i in information_list:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена(user_token)')

    def age_low(self, user_id): #Получение минимального возраста человека, для поиска
        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
                date_list = date.split('.')
                if len(date_list) == 3:
                    year = int(date_list[2])
                    year_now = int(datetime.date.today().year)
                    return year_now - year
                elif len(date_list) == 2 or date not in information_list:
                    self.write_msg(user_id, 'Введи минимальный возраст поиска: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена (user_token)')

    def age_high(self, user_id): #Получение минимального возраста человека, для поиска

        url = url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введи максимальный возраст человека, для поиска: ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
                    else:
                        break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def cities(self, user_id, city_name):
        url = url = f'https://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                    'country_id': 1,
                    'q': f'{city_name}',
                    'need_all': 0,
                    'count': 1000,
                    'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')


    def get_city(self, user_id): #Получение города, для поиска
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введи название твоего города: ')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_user(self, user_id): #Поиск пользователей

        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.age_low(user_id),
                  'age_to': self.age_high(user_id),
                  'city': self.get_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            resp_person_dict = resp_json['response']
            resp_person_list = resp_person_dict['items']
            for person_dict in resp_person_list:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = 'vk.com/id' + str(person_dict.get('id'))
                else:
                    continue
            return f'Поиск завершён'
        except KeyError:
            self.write_msg(user_id, 'Почему выводиться ошибка??')

    def get_photos(self, user_id): #Получение фото пользователей

        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        try:
            resp_person_dict = resp_json['response']
            resp_person_list = resp_person_dict['items']
            for i in resp_person_list:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photo_full(self, user_id): #Получение id фотографий
        list = self.get_photos(user_id)
        count = 0
        for i in list:
            count += 1
            if count <= 3:
                return i[1]


    def send_photo_3(self, user_id, message, offset):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': access_token_group,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_{self.get_photo_full(self.person_id(offset))}',
                                         'random_id': 0})




bot =VKBot();
