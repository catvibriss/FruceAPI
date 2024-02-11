from .objects import *
from . import exceptions
import aiohttp

# Тут главное

class Client:
    def __init__(self, token: str):
        self.token = token
        self.url = 'https://api.fruitspace.one/v2/'
        self.headers = {
            "Authorization": token
        }

    async def get_user_info(self):
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'user', headers=self.headers)
            json = await req.json()
            return json

    async def fetch_gdps(self, gdpsid, expiry_date=None):
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'fetch/gd/info/'+gdpsid, headers=self.headers)
            json = await req.json()
            json['expire_date'] = expiry_date
            return Server(json)

    async def get_user_servers(self):
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+'servers', headers=self.headers)
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            servers = []
            for srv in json['gd']:
                servers.append(await self.fetch_gdps(srv['srvid'], srv['expire_date']))
            return servers

    async def get_gdps_config(self, gdps):
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.url+f'servers/gd/{gdps}', headers=self.headers)
            json = await req.json()
            if 'status' in json:
                if json['status'] == 'error':
                    if json['message'] == 'You have no permission to manage this server':
                        raise exceptions.NoPermissionError('You have no permission to manage this server')
                    elif json['message'] == 'Unauthorized':
                        raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

    async def delete_gdps(self, gdps):
        async with aiohttp.ClientSession() as session:
            req = await session.delete(self.url+f'servers/gd/{gdps}', headers=self.headers)
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

    async def get_gdps_logs(self, gdps: str, type: int, page: int):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+f'servers/gd/{gdps}/logs', headers=self.headers, data={'type': type, 'page': page})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

    async def upload_music(self, gdps: str, type: str, url: str):
        async with aiohttp.ClientSession() as session:
            req = await session.put(self.url+f'servers/gd/{gdps}/music', headers=self.headers, data={'type': type, 'url': url})
            json = await req.json()
            if json['status'] == 'error':
                if json['message'] == 'You have no permission to manage this server':
                    raise exceptions.NoPermissionError('You have no permission to manage this server')
                elif json['message'] == 'Unauthorized':
                    raise exceptions.UnauthorizedError('You\'re unauthorized')
            return json

class GDPS:
    def __init__(self, gdps: str):
        self.url = f'https://rugd.gofruit.space/{gdps}/db/'

    async def get_user(self, accid: int):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJUserInfo20.php', data={"secret": "Wmfd2893gb7", "targetAccountID": accid})
            text = await req.text()
            return User(text)

    async def download_level(self, levelid: int):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'downloadGJLevel22.php', data={"secret": "Wmfd2893gb7", "levelID": levelid})
            return Level(await req.text())

    async def get_comments(self, levelid):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url + 'getGJComments21.php', data={"secret": "Wmfd2893gb7", "levelID": levelid, "page": 0})
            text = await req.text()
            comments = []
            
            return comments

    async def get_acc_comments(self, userid: int, page: int):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url + 'getGJAccountComments20.php', data={"secret": "Wmfd2893gb7", "accountID": userid, "page": page})
            acs = []
            text = await req.text()
            for ac in text.split('#')[0].split('|'):
                acs.append(AccComment(ac))
            return acs

    async def register_account(self, username: str, password: str, email: str):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'accounts/registerGJAccount.php', data = {
                "userName": username,
                "password": password,
                "email": email,
                "secret": "Wmfv3899gc9"
            })
            return await req.text()

    async def get_song(self, song_id):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJSongInfo.php', data = {
                "secret": "Wmfd2893gb7",
                "songID": song_id
            })
            return Song(await req.text())

    async def get_daily(self):
        async with aiohttp.ClientSession() as session:
            return await self.download_level(-1)
    async def get_weekly(self):
        return await self.download_level(-2)

    async def get_user_with_username(self, username):
        async with aiohttp.ClientSession() as session:
            req = await session.post(self.url+'getGJUsers20.php', data={"secret": "Wmfd2893gb7", "str": username})
            text = await req.text()
            req2 = await self.get_user(int(text.split(':')[3]))
            return req2
