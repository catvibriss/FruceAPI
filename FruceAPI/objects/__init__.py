from .. import utils
from urllib.parse import unquote
import base64


class Song:
    def __init__(self, rawdata: str):
        args = rawdata.replace('~', '').split('|')
        self.id = args[1]
        self.song_name = args[3]
        self.artist = args[7]
        self.size = args[9]
        self.url = unquote(args[13])

class SongResponse:
    def __init__(self, json: dict):
        self.artist = json['artist']
        self.id = json['id']
        self.author_id  = json['author_id']
        self.name = json['name']
        self.is_banned = json['is_banned']
        self.size = json['size']
        self.url = json['url']

class AccComment:
    def __init__(self, rawdata):
        args = rawdata.split('~')
        self.comment = base64.b64decode(args[1]).decode()
        self.uid = args[3]
        self.likes = args[5]
        self.age = args[13]

class Comment:
    def __init__(self, rawdata):
        targs = rawdata.split(':')
        print(rawdata, targs)
        args = targs[0].split('~')
        self.comment = base64.b64decode(args[1]).decode()
        self.uid = args[3]
        self.id = args[9]
        self.is_spam = args[11]
        self.percent = args[17]
        self.ago = args[15]
        self.sender = targs[1].split('~')[1]

class Level:
    def __init__(self, rawdata):
        args = rawdata.split('#')[0]
        args = rawdata.split(':')
        self.id = args[1]
        self.name = args[3]
        self.description = base64.b64decode(args[5]).decode()
        self.level_string = utils.decode_level(args[7], False)
        self.version = args[9]
        self.authorid = args[11]
        self.difficulty = args[13]
        self.downloads = args[17]
        self.track_id = args[19]
        self.version_game = args[21]
        self.likes = args[23]
        self.length = args[25]
        self.demon_difficulty = args[61]
        self.stars = args[29]
        self.is_featured = args[31]
        self.auto = args[33]
        self.password = args[35]
        self.upload_date = args[37]
        self.update_date = args[39]
        self.orig_id = args[41]
        self.is_2players = args[43]
        self.song_id = args[45]
        self.ucoins = args[49]
        self.coins = args[51]
        self.stars_requested = args[53]
        self.is_ldm = args[55]
        self.is_epic = args[57]
        self.objects = args[63]

class User:
    def __init__(self, rawdata):
        args = rawdata.split(':')
        self.uname = args[1]
        self.uid = args[3]
        self.stars = args[5]
        self.demons = args[7]
        self.leaderboard_rank = args[9]
        self.cpoints = args[11]
        self.icon = args[13]
        self.color_primary = args[15]
        self.color_secondary = args[17]
        self.coins = args[19]
        self.icon_type = args[21]
        self.special = args[23]
        self.ucoins = args[29]
        self.youtube = args[35]
        self.cube = args[37]
        self.ship = args[39]
        self.ball = args[41]
        self.ufo = args[41]
        self.wave = args[43]
        self.robot = args[45]
        self.trace = args[47]
        self.spider = args[55]
        self.twitter = args[57]
        self.twitch = args[59]
        self.diamonds = args[63]
        self.death = args[65]

class Server:
    def __init__(self, json: dict):
        self.srvid = json['srvid']
        if json['plan'] == 1:
            self.plan = 'Press Start'
        elif json['plan'] == 2:
            self.plan = 'Singularity'
        elif json['plan'] == 3:
            self.plan = 'Takeoff'
        self.srv_name = json['srv_name']
        self.owner_id = json['owner_id']
        self.user_count = json['user_count']
        self.level_count = json['level_count']
        self.client_android_url = json['client_android_url']
        self.client_ios_url = json['client_ios_url']
        self.client_windows_url = json['client_windows_url']
        self.client_macos_url = json['client_macos_url']
        self.icon = json['icon']
        self.description = json['description']
        self.text_align = json['text_align']
        self.discord = json['discord']
        self.vk = json['vk']
        self.version = json['version']
        self.is_custom_textures = json['is_custom_textures']

class List:
    def __init__(self, rawdata: str):
        args = rawdata.split(':')
        self.id = args[1]
        self.name = args[3]
        self.description = base64.b64decode(args[5])
        self.author = args[11]
        self.downloads = args[13]
        self.likes = args[17]
        self.levels = args[21].split(',')
        
class Node:
    def __init__(self, data: str):
        args = data.split(',')
        self.name = args[1]
        self.id = args[3]
        self.type = 'track' if args[5] == '0' else 'folder'
        if len(args) > 7:
            self.parent_node = args[7]
            self.size = args[9]

class Srv:
    def __init__(self, json):
        self.srvid = json['srvid']
        self.srv_name = json['srv_name']
        self.plan = {1: 'Press Start', 2: 'Singularity', 3: 'Takeoff'}[json['plan']]
        self.owner_id = json['owner_id']
        self.user_count = json['user_count']
        self.level_count = json['level_count']
        self.comment_count = json['comment_count']
        self.post_count = json['post_count']
        self.creation_date = json['creation_date']
        self.expire_date = json['expire_date']
        self.client_android_url = json['client_android_url']
        self.client_windows_url = json['client_windows_url']
        self.client_ios_url = json['client_ios_url']

class Tariff:
    def __init__(self, json):
        self.title = json['Title']
        self.price_rub = json['PriceRUB']
        self.price_usd = json['PriceUSD']


class GDPSConfig:
    def __init__(self, json):
        self.srv = Srv(json['Srv'])
        self.tariff = Tariff(json['Tariff'])