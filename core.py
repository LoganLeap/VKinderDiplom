from pprint import pprint
from datetime import datetime
# импорты
import vk_api
from vk_api.exceptions import ApiError
import requests
from config import acces_token


# получение данных о пользователе


class VkTools:
    def __init__(self, acces_token):
        self.vkapi = vk_api.VkApi(token=acces_token)

    def _bdate_toyear(self, bdate):
        user_year = bdate.split('.')[2]
        now = datetime.now().year
        return now - int(user_year)

    def get_user(user_id, access_token):
        url = "https://api.vk.com/method/users.get?user_ids={0}&fields=photo_400_orig&v=5.60".format(user_id)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Content-Encoding': 'utf-8'}

        res = requests.get('https://api.vk.com/method/account.getProfileInfo?user_ids={0}&access_token={1}'.
                           format(user_id, access_token), headers=headers)
        print(res.json())
        if 'error' not in res.json():
            try:
                response = requests.get(url, headers=headers)
                city = response.json()['response'][0]['city']
            except Exception as e:
                print(e)
                city = None
            user = res.json()['response']
            name = user['first_name']
            vk_id = 'vk_' + str(user_id)
            sex = user['sex'] or 0

            if 'home_town' in user:
                city = user['home_town']
            elif 'city' in user:
                city = user['city']['title']
            else:
                city = None


            return {'name': name, 'sex': sex, 'city': city, 'id': vk_id}
        return False
    def get_profile_info(self, user_id):

        try:
            info = self.vkapi.method('users.get',
                                      {'user_id': user_id,
                                       'fields': 'city,sex,relation,bdate'
                                       }
                                      )
        except ApiError as e:
            info = params
            print(f'error = {e}')

        result = {'name': (info['first_name'] + ' ' + info['last_name']) if
                  'first_name' in info and 'last_name' in info else None,
                  'sex': info.get('sex'),
                  'city': info.get('city')['title'] if info.get('city') is not None else None,
                  'year': self._bdate_toyear(info.get('bdate'))
                  }
        sex = ('sex')
        city = ('city')
        year = ('year')
        return result

    def search_worksheet(self, params, offset):
        try:
            users = self.vkapi.method('users.search',
                                      {
                                          'count': 10,
                                          'offset': offset,
                                          'hometown': params['city'],
                                          'sex': 1 if 'sex' == 1 else 1,
                                          'has_photo': True,

                                      }
                                      )
        except ApiError as e:
            users = []
            print(f'error = {e}')

        result = [{'name': item['first_name'] + item['last_name'],
                   'id': item['id']
                   } for item in users['items'] if item['is_closed'] is False
                  ]

        return result

    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'owner_id': id,
                                        'album_id': 'profile',
                                        'extended': 1
                                        }
                                       )
        except ApiError as e:
            photos = {}
            print(f'error = {e}')

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count']
                   } for item in photos['items']
                  ]

        '''мой код'''
        def result_sort(i):
            return ((i.get('likes'))+ (i.get('comments')))
        return sorted(result, key=result_sort, reverse=True)[:3]
        '''мой код'''

if __name__ == '__main__':
    user_id = 789657038
    tools = VkTools(acces_token)
    params = tools.get_user(user_id)
    worksheets = tools.search_worksheet(params, 20)
    worksheet = worksheets.pop()
    photos = tools.get_photos(worksheet['id'])

    pprint(worksheets)


