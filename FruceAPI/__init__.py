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

class Hosting:
    """
    ## Класс Hosting
    Для его работы не потребуется токен так как он возвращает общедоступную информацию
    """
    def __init__(self):
        self.base_url = 'https://api.fruitspace.one/v2/'
        self.headers = {
        }   

    async def fetch_gdps(self, gdpsid: str) -> Server:
        '''
### Функция ищет общедоступную информацию о GDPS сервере по его ID

Аргументы:
* gdpsID : str\n
    ID сервера из 4 символов
---
Возвращает обьект `Server`
        '''

        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+'fetch/gd/info/'+gdpsid)
            json = await req.json()
            return Server(json)
    
    async def top_gdps(self, offset: int = 0) -> list[Server]:
        '''
        ### Функция возвращает список самых крупных серверов FruitSpace
        
        Аргументы:
        * offset : int\n
            Отступ от верха списка. Например если offset равен 5 то первым в списке будет топ-5 сервер, затем топ-6 и т.д.
        ---
        Возвращает список с объектами `Server`
        '''
        
        async with aiohttp.ClientSession() as session:
            if offset < 0:
                offset = 0
            req = await session.get(self.base_url+f'fetch/gd/top?offset={offset}')
            json = await req.json()
            if json['status'] == 'ok':
                return [await self.fetch_gdps(i['srvid']) for i in json['servers']]

class MusicType:
    YouTube = "yt"
    VK = "vk"
    NewGround = "ng"
    Deezer = "dz"
    DataBase = "db"   

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
        self.base_url = 'https://api.fruitspace.one/v2/'
        self.headers = {
            "Authorization": token
        }
    # TODO: на след. обнову
    async def get_gpds_roles(self, gdpsid: str) -> dict:
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+f'servers/gd/{gdpsid}/roles', headers=self.headers)
            json = await req.json()
            return json

    async def get_user_info(self) -> dict:
        '''
### Функция для получения данных о аккаунте FruitSpace

Возвращает словарь с данными
        '''

        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+'user', headers=self.headers)
            json = await req.json()
            return json

    async def get_user_servers(self) -> list[Server]:
        '''
### Функция для получения всех GDPS серверов пользователя

Возвращает список с обьектами `Server`
        '''
        
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+'servers', headers=self.headers)
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            servers = []
            for srv in json['gd']:
                servers.append(await Hosting().fetch_gdps(srv['srvid']))
            return servers

    async def delete_gdps(self, gdpsid: str) -> str:
        '''
### Функция для удаления GDPS сервера
## Осторожно! Сервер удаляется без возможности восстановления!

Аргументы:
* gdpsID : str\n
    ID сервера из 4 символов
---
Возвращает либо ошибку, либо сообщение об успешном удалении сервера 
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.delete(self.base_url+f'servers/gd/{gdpsid}', headers=self.headers)
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

Аргументы:
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
            req = await session.post(self.base_url+f'servers/gd/{gdpsid}/logs', headers=self.headers, data={'type': type, 'page': page})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

    async def upload_music(self, gdpsid: str, type: str, url: str) -> SongResponse:
        '''
### Функция для загрузки музыки на сервер

Аргументы:
* gdpsID : str\n
    ID сервера из 4 символов
* type : str\n
    Тип загружаемой музыки
    `ng` (newgrounds), `yt` (youtube), `vk` (vkontakte), `dz` (deezer), `db` (dropbox/direct links)
* url : str\n
    Ссылка для добавления
        '''
        if len(url) == 0:
            raise AttributeError('Empty music link')
        if not type in ['ng', 'yt', 'vk', 'dz', 'db']:
            raise TypeError('Wrong music type')

        async with aiohttp.ClientSession() as session:
            req = await session.put(self.base_url+f'servers/gd/{gdpsid}/music', headers=self.headers, data={'type': type, 'url': url})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
                elif json['message'] == 'music not found':
                    raise exceptions.MusicNotFoundError('Music not found')
            return SongResponse(json=json['music'])
       
    async def get_gdps_config(self, gdpsid: str) -> GDPSConfig:
        '''
        ### Функция получает приватную и более расширенную информацию о вашем сервере чем фукнкция `fetch_gdps()`

        Аргументы:
        * gdpsid : str
            ID сервера состоящий из 4 символов
        ---
        Возвращает объект `GDPSConfig`
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+f'servers/gd/{gdpsid}', headers=self.headers)
            json = await req.json()
            if 'status' in json:
                if json['status'] == 'error':
                    if json['message'] == 'You have no permission to manage this server':
                        raise exceptions.NoPermissionError('You have no permission to manage this server')
                    elif json['message'] == 'Unauthorized':
                        raise exceptions.UnauthorizedError('You\'re unauthorized')
                    
            return GDPSConfig(json)
        
    async def create_gdps(self, name: str, tariff: int = 1, promocode: str = '') -> str:
        '''
        ### Функция позволяет создать сервер на хостинге FruitSpace
        
        Если вы хотите создавать платные сервера, убедитесь что у вас достаточно денег на балансе

        Аргументы:
        * name : str\n
            Название сервера
        * tariff : int\n
            Тариф сервер от 1 до 3\n
            1 - Press Start\n
            2 - Singularity\n
            3 - Takeoff\n
        * promocode : str\n
            Промокод для покупки. Необязательно
        ---
        Возвращает либо ошибку, либо успешный статус создания сервера вместе с его ID
        '''
        if tariff not in [1,2,3]:
            raise TypeError('Invalid Tariff')
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url+'servers/gd', headers=self.headers, data={
  "duration": "string",
  "name": name,
  "promocode": promocode,
  "srvid": "",
  "tariff": tariff})
            json = await req.json()
            if json['status'] == 'ok':
                return f"Server created succsessful!\nID: {json['message']}\nName: {name}\nTariff: {tariff}"
            if json['status'] == 'error':
                    if json['message'] == 'You have no permission to manage this server':
                        raise exceptions.NoPermissionError('You have no permission to manage this server')
                    elif json['message'] == 'Unauthorized':
                        raise exceptions.UnauthorizedError('You\'re unauthorized')
                    elif json['message'] == 'You already have FREE server':
                        raise exceptions.AlreadyHaveFreeServer('There can only be one free server on one account')
                    elif json['code'] == 'bal':
                        raise exceptions.NotMoneyOnBalance('There are not enough funds to purchase a server')
                    else:
                        return json

class GDPS:
    """
## Класс GDPS
Используется для работы с GDPS серверами. Для работы нужен ID сервера  

---
## Атрибуты класса:
    gdpsid : str\n
        ID сервера для взаимодействия

    """
    def __init__(self, gdpsid: str):
        self.base_url = f'https://rugd.gofruit.space/{gdpsid}/db/'
   
    async def get_user(self, accid: int) -> User:
        '''### Поиск пользователя по его ID
        
Аргументы:
* accid : int\n
    UID пользователя для поиска
---
Возвращает объект `User`
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url+'getGJUserInfo20.php', data={"secret": "Wmfd2893gb7", "targetAccountID": accid})
            text = await req.text()
            return User(text)
        
    async def download_level(self, levelid: int) -> Level:
        '''### Поиск уровня по его ID

        Аргументы:
        * levelid : int\n
            ID уровня для поиска
        ---
        Возвращает обьект `Level`'''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url+'downloadGJLevel22.php', data={"secret": "Wmfd2893gb7", "levelID": levelid})
            return Level(await req.text())
     
    async def get_comments(self, levelid: int) -> list[Comment]:
        """
        ### Функция для получения комментариев из уровня

        Аргументы:
        * levelid : int\n
            ID уровня для поиска
        ---
        Возвращает список с обьектами `Comment`
        """
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url + 'getGJComments21.php', data={"secret": "Wmfd2893gb7", "levelID": levelid, "page": 0})
            text = await req.text()
            comments = []
            for c in text.split('|'):
                try:
                    comments.append(Comment(c))
                except:
                    pass
            
            return comments
    
    async def get_acc_comments(self, userid: int, page: int) -> list[AccComment]:
        """
        ### Функция для получения комментариев пользователя

        Аргументы:
        * userid : int\n
            UID пользователя 
        * page : int\n
            Страница с комментариями
        ---
        Возвращает список с обьектами `AccComment`"""
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url + 'getGJAccountComments20.php', data={"secret": "Wmfd2893gb7", "accountID": userid, "page": page})
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
            req = await session.post(self.base_url+'accounts/registerGJAccount.php', data = {
                "userName": username,
                "password": password,
                "email": email,
                "secret": "Wmfv3899gc9"
            })
            return await req.text()
    
    async def get_song(self, songid: int) -> Song:
        '''
        ### Получить песню по ID
        
        Аргументы:
        * songid : int\n
            ID песни для поиска
        ---
        Возвращает обьект `Song`
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url+'getGJSongInfo.php', data = {
                "secret": "Wmfd2893gb7",
                "songID": songid
            })
            return Song(await req.text())
    
    async def get_daily(self) -> Level:
        '''### Поиск ежедневного уровня

        Возвращает обьект `Level` '''
        async with aiohttp.ClientSession() as session:
            return await self.download_level(-1)

    async def get_weekly(self) -> Level:
        '''### Поиск еженедельного уровня

        Возвращает обьект `Level` '''
        async with aiohttp.ClientSession() as session:
            return await self.download_level(-2)
    
    async def get_user_with_username(self, username: str) -> User:
        '''### Поиск пользователя по его никнейму
        
Аргументы:
* username : str\n
    Никнейм пользователя для поиска
---
Возвращает объект `User`
        '''
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.base_url+'getGJUsers20.php', data={"secret": "Wmfd2893gb7", "str": username})
            text = await req.text()
            req2 = await self.get_user(int(text.split(':')[3]))
            return req2
    
    async def get_custom_content_url(self) -> str:
        """
        ### Получение ссылки для кастомных SFX
        
        Возвращает ссылку, которую можно использовать в функции `download_sfx_lib`"""
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+'getCustomContentURL.php')
            return await req.text()
    
    async def download_sfx_lib(self, content_url: str = None) -> list[Node]:
        """
        ### Получение SFX бибилиотеки

        Аргументы:
        * content_url : str
            Ссылка для кастомных эффектов сервера. Можно ничего не указывать и функция автоматически получит ссылку для сервера, ID которого вы указали прни вызове класса GDPS
        ---
        Возвращает список с обьектами `Node`
        """
        async with aiohttp.ClientSession() as session:
            if content_url != None:
                req = await session.get(content_url+'/sfx/sfxlibrary.dat')
            else:
                link = await self.get_custom_content_url()
                req = await session.get(link+'/sfx/sfxlibrary.dat')
            content = await req.text()
            data = content.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            decompressed_data = zlib.decompress(decoded_data)
            sfxlib = []
            for sfx in str(decompressed_data).split(';'):
                try:
                    sfxlib.append(Node(sfx))
                except:
                    pass
            return sfxlib

    # TODO: понять что это за хуйня вообще
    '''
    async def get_level_lists(self, stype: str = "likes") -> List:
        """
        ### Бог знает что это за функция

        Аргументы:\n
        * stype : str
            Фильтр для поиска: 'likes', 'downloads', 'recent', 'featured', 'recently awarded'
        ---
        Возвращает обьект `List` (это не список)"""
        if stype not in ['likes', 'downloads', 'recent', 'featured', 'recently awarded']:
            raise TypeError('The wrong type of filter')
        types = {'likes': 0, 'downloads': 1, 'recent': 4, 'featured': 6, 'recently awarded': 11}
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.base_url+'getGJLevelLists.php', data={'secret': 'Wmfd2893gb7', 'type':str(types[stype])}, headers={'User-Agent':''})
            text = await req.text()
            lists = []
            for list in text.split('|'):
                try:
                    lists.append(List(list))
                except:
                    pass
            return lists
    '''

# ну это пиздец друзья