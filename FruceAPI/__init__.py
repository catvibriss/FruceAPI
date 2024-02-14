"""
# FruceAPI
Данная библиотека предназначена для простой и удобной работы с хостингом FruitSpace

Подробная документация: https://miwco.gitbook.io/fruceapi/

Разработчики: nosleepfortonight & kot_v_palto
"""

from .objects import *
from . import exceptions
import aiohttp
import zlib

class Client:
    """
## Класс Client
Используется для работы с хостином FruitSpace. Для работы нужен токен вашего аккаунта с сайта FruitSpace  

---
## Атрибуты класса:
    token : str
        токен вашего аккаунта с FruitSpace

    """

    def __init__(self, token: str):
        self.token = token
        self.url = 'https://api.fruitspace.one/v2/'
        self.headers = {
            "Authorization": token
        }

    async def get_user_info(self) -> dict:
        '''
### Функция для получения данных о аккаунте FruitSpace

Возвращает словарь с данными
        '''

        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'user', headers=self.headers)
            json = await req.json()
            return json

    async def get_user_servers(self) -> list[Server]:
        '''
### Функция для получения всех GDPS серверов пользователя

Возвращает список с обьектами `Server`
        '''
        
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'servers', headers=self.headers)
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            servers = []
            for srv in json['gd']:
                servers.append(await self.fetch_gdps(srv['srvid']))
            return servers

    async def fetch_gdps(self, gdpsid: str) -> Server:
        '''
### Функция ищет общедоступную информацию о GDPS сервере по его ID

Параметры:
* gdpsID : str
    ID сервера из 4 символов
---
Возвращает обьект `Server`
        '''

        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'fetch/gd/info/'+gdpsid, headers=self.headers)
            json = await req.json()
            return Server(json)

    async def delete_gdps(self, gdpsid: str) -> str:
        '''
### Функция для удаления GDPS сервера
## Осторожно! Сервер удаляется без возможности восстановления!

Параметры:
* gdpsID : str
    ID сервера из 4 символов
---
Возвращает либо ошибку, либо сообщение об успешном удалении сервера 
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.delete(self.url+f'servers/gd/{gdpsid}', headers=self.headers)
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            elif json['status'] == 'ok':
                return f'The GDPS "{gdpsid}" was deleted successfully'

    async def get_gdps_logs(self, gdpsid: str, type: int, page: int) -> dict:
        '''
### Функция для получения логов GDPS

Параметры:
* gdpsID : str\n
    ID сервера из 4 символов
* type : int\n
    Тип логов:
        Есть несколько типов логов:
        * -1 - все логи
        * 0 - регистрации
        * 1 - входы
        * 2 - удаление аккаунтов
        * 3 - баны
        * 4 - действия с уровнями
* page : int\n
    Страница логов

Возвращает словарь с логами
* count - количество полученных логов 
* message - сообщение от хостинга
* status - полученный статус от хостинга (если будет `error` выйдет ошибка)
* result - список с логами
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+f'servers/gd/{gdpsid}/logs', headers=self.headers, data={'type': type, 'page': page})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

    async def upload_music(self, gdpsid: str, type: str, url: str):
        '''
### Функция для загрузки музыки на сервер

Параметры:
* gdpsID : str\n
    ID сервера из 4 символов
* type : str\n
    Тип загружаемой музыки
    `ng` (newgrounds), `yt` (youtube), `vk` (vkontakte), `dz` (deezer), `db` (dropbox/direct links)
* url : str\n
    Ссылка для добавления
        '''
        if not type in ['ng', 'yt', 'vk', 'dz', 'db']:
            raise TypeError('Wrong music type')

        async with aiohttp.ClientSession() as session:
            req = await session.put(self.url+f'servers/gd/{gdpsid}/music', headers=self.headers, data={'type': type, 'url': url})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
                elif json['message'] == 'music not found':
                    raise exceptions.MusicNotFoundError('Music not found')
            return SongResponse(json)
        
    # TODO: fix + doc
    '''
    async def get_gdps_config(self, gdpsID: str):
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+f'servers/gd/{gdpsID}', headers=self.headers)
            json = await req.json()
            if 'status' in json:
                if json['status'] == 'error':
                    if json['message'] == 'You have no permission to manage this server':
                        raise exceptions.NoPermissionError('You have no permission to manage this server')
                    elif json['message'] == 'Unauthorized':
                        raise exceptions.UnauthorizedError('You\'re unauthorized')
            return GDPSConfig(json)'''

class GDPS:
    """
## Класс GDPS
Используется для работы с GDPS серверами. Для работы нужен ID сервера  

---
## Атрибуты класса:
    gdpsid : str
        ID сервера для взаимодействия

    """
    def __init__(self, gdpsid: str):
        self.url = f'https://rugd.gofruit.space/{gdpsid}/db/'
   
    async def get_user(self, accid: int) -> User:
        '''Поиск пользователя по его ID'''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJUserInfo20.php', data={"secret": "Wmfd2893gb7", "targetAccountID": accid})
            text = await req.text()
            return User(text)
        
    async def download_level(self, levelid: int) -> Level:
        '''Поиск уровня по его ID
        Возвращает обьект `Level`'''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'downloadGJLevel22.php', data={"secret": "Wmfd2893gb7", "levelID": levelid})
            return Level(await req.text())
     
    async def get_comments(self, levelid: int) -> list:
        """
        Функция возвращает список с комментариями из уровня
        """
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url + 'getGJComments21.php', data={"secret": "Wmfd2893gb7", "levelID": levelid, "page": 0})
            text = await req.text()
            comments = []
            for c in text.split('|'):
                try:
                    comments.append(Comment(c))
                except:
                    pass
            
            return comments
    
    async def get_acc_comments(self, userid: int, page: int) -> list[AccComment]:
        '''Возвращает список с обьектами `AccComments`'''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url + 'getGJAccountComments20.php', data={"secret": "Wmfd2893gb7", "accountID": userid, "page": page})
            acs = []
            text = await req.text()
            for ac in text.split('#')[0].split('|'):
                acs.append(AccComment(ac))
            return acs
    
    async def register_account(self, username: str, password: str, email: str) -> None:
        '''## Регистрация пользователя на сервере\n  
        Список с ошибками:
        * 1 - аккаунт создан успешно
        * -1 - данные вписаны не до конца (например вместо имени пустая строка)
        * -2 - аккаунт с таким именем уже существует
        * -3 - аккаунт с такой почтой уже существует'''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'accounts/registerGJAccount.php', data = {
                "userName": username,
                "password": password,
                "email": email,
                "secret": "Wmfv3899gc9"
            })
            return await req.text()
    
    async def get_song(self, songid: int) -> Song:
        '''
        ## Получить песню по ID
        
        Возвращает обьект `Song`
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJSongInfo.php', data = {
                "secret": "Wmfd2893gb7",
                "songID": songid
            })
            return Song(await req.text())
    
    async def get_daily(self) -> Level:
        '''
        Получить ежедневный уровень

        Возвращает обьект `Level`
        '''
        async with aiohttp.ClientSession() as session:
            return await self.download_level(-1)

    async def get_weekly(self) -> Level:
        '''
        Получить еженедельный уровень
        
        Возвращает обьект `Level`
        '''
        async with aiohttp.ClientSession() as session:
            return await self.download_level(-2)
    
    async def get_user_with_username(self, username: str) -> User:
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJUsers20.php', data={"secret": "Wmfd2893gb7", "str": username})
            text = await req.text()
            req2 = await self.get_user(int(text.split(':')[3]))
            return req2
    
    # TODO: beauty + doc
    '''
    async def get_custom_content_url(self):
        """Получить URL контента такого как sfx или библиотека музыка"""
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'getCustomContentURL.php')
            return await req.text()'''
    # TODO: tests + doc
    '''
    async def get_level_lists(self, stype: str = "likes") -> List:
        """
        stype - то, по чему искать: 'likes', 'downloads', 'recent', 'featured', 'recently awarded'"""
        types = {'likes': 0, 'downloads': 1, 'recent': 4, 'featured': 6, 'recently awarded': 11}
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'getGJLevelLists.php', data={'secret': 'Wmfd2893gb7', 'type':str(types[stype])}, headers={'User-Agent':''})
            text = await req.text()
            lists = []
            for list in text.split('|'):
                try:
                    lists.append(List(list))
                except:
                    pass
            return lists'''
    # TODO: doc
    '''
    async def download_sfx_lib(self, content_url: str) -> list[Node]:
        """
        Скачать sfx библиотеку"""
        async with aiohttp.ClientSession() as session:
            req = await session.get(content_url+'/sfx/sfxlibrary.dat')
            content = await req.text()

            # Replace "-" with "+" and "_" with "/"
            data = content.replace("-", "+").replace("_", "/")

            # Decode base64
            decoded_data = base64.b64decode(data)

            # Decompress using zlib
            decompressed_data = zlib.decompress(decoded_data)
            sfxlib = []
            # Print or use the decompressed data as needed
            for sfx in str(decompressed_data).split(';'):
                try:
                    sfxlib.append(Node(sfx))
                except:
                    pass # no smash
            return sfxlib'''
