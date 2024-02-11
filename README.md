# FruceAPI
FruceAPI - это удобный инструмент для работы с хостингом FruitSpace  
Данная библиотека *не является официальной* и не создана разработчиками FruitSpace

# ДОКУМЕНТАЦИЯ НЕ ПОЛНАЯ!!!! КОГДА БУДЕТ НАПИСАНА ПОЛНОСТЬЮ ЭТОТ ТЕКСТ ИСЧЕЗНЕТ!!!

# С чего начать
Сначала нужно установиьт FruceAPI на ваш компьютер. Для этого пропишите в консоли эту команду
```py
pip install FruceAPI
```
#### Теперь мы можем написать первую программу на FruceAPI!
```py
import FruceAPI as FRAPI # импортируем FruceAPI
from asyncio import run # импортируем библиотеку для запуска асинхронной функции

client = FRAPI.Client("token") # класс клиента для работы с FruitSpace
# token - это ваш токен на FruitSpace
# НИКОМУ НЕ ДАВАЙТЕ ЭТОТ ТОКЕН (ДАЖЕ КОТУ)!!!
async def about_user(): 
    user = await client.get_user_info() # получаем информацию о пользователе
    print(f"Ваш никнейм: {user['uname']}") # выводим имя пользователя

run(about_user()) # запускаем асинхронную функцию
```
Обратите внимание что `get_user_info()`, как и все остальные функции в FruceAPI, это `corotuine` функция  
Если вы всё сделали правильно, то в консоли вы увидите имя вашего аккаунта на FruitSpace
```
Ваш никнейм: Nickname
```

# Client Class
> Данный класс предназначен для работы с FruitSpace  
> Для работы понадобится Ваш токен  

### Получение GDPS сервера
```py
import FruceAPI as FRAPI
from asyncio import run

client = FRAPI.Client("token")

async def get_gdps():
    gdps = await client.fetch_gdps(gdpsid='0015') # указываем ID сервера
    # Функция fetch_gdps выдает общедоступные данные, поэтому при её вызове необязательно писать токен в client
    print(f"Название сервера: {gdps.name}")
    print(f"ID сервера: {gdps.srvid}")

run(get_gdps())
```
Функция `fetch_gdps` возвращает обьект `Server`, и с помощью атрибутов `name` и `srvid` мы получиди в консоли это сообщение:
```
Название сервера: KotGDPS
ID сервера: 0015
```
*тут будет полный список атрибутов*
***
### Получение всех серверов по токену
***
### Добавление музыки на GDPS
***
### Удаление GDPS
***
### Получение логов GDPS
***
# GDPS class
> Данный класс позволяет работать с данными из GDPS и не требует введения токена FruitSpace   
### Получение данных про игрока
```py
import FruceAPI as FRAPI
from asyncio import run

gdps = FRAPI.GDPS('0015') # Подключаем GDPS по ID сервера

async def get_gdps_user():
    # user = await gdps.get_user(1) # для поиска по UID
    user = await gdps.get_user_with_username("Kotvpalto") # для поиска по никнейму
    # выводим полученные данные
    print(f"UID игрока: {user.uid}")
    print(f"Никнейм игрока: {user.uname}")
    print(f"Звёзды игрока: {user.stars}")

    user_comments = await gdps.get_acc_comments(userid=1, page=0)
    # userid - UID игрока
    # page - страница с комментариями
    # функция возвращает список обьектов AccComment
    print(f"Комментарий: {user_comments[0].comment}")
    print(f"Лайки: {user_comments[0].likes}")

run(get_gdps_user())
```
Поиск игрока по его UID и по его никнейму возвращает одинаковый тип данных - `User`  
*тут будет полный список атрибутов User*
*тут будет полный список атрибутов AccComment*
***
### Получение данных про уровень
```py
import FruceAPI as FRAPI
from asyncio import run

gdps = FRAPI.GDPS('0015') # Подключаем GDPS по ID сервера

async def get_gdps_level():
    level = await gdps.download_level(1) # указываем ID уровня

    print(f"ID уровня: {level.id}")
    print(f"Название уровня: {level.name}")
    print(f"Длина уровня: {level.length}")
    # lenght возвращает числовое значение от 0 до 5
    # 0 - tiny / 1 - short / 2 - meduim /
    # 3 - long / 4 - XL / 5 - platformer

    level_comments = await gdps.get_comments(1) # указываем ID уровня
    # Для получения комментариев используется функция get_comments()
    print(level_comments) # возвращется список с комментариями

    daily_level = await gdps.get_daily()
    weekly_level = await gdps.get_weekly()
    # get_daily и get_weekly возвращают тип данных Level

run(get_gdps_level())
```
*Примечание: функция get_comments() не работает*  
Поиск уровня по его ID возвращает тип данных - `Level`    
*тут будет полный список атрибутов*
***
### Получение данных о песне
```py
import FruceAPI as FRAPI
from asyncio import run

gdps = FRAPI.GDPS('0015') # Подключаем GDPS по ID сервера

async def get_gdps_level():
    song = await gdps.get_song(song_id=51) # указывается ID песни

    print(f"Название песни: {song.song_name}")
    print(f"Автор: {song.artist}")

run(get_gdps_level())
```
Поиск песни по её ID возвращает тип данных - `Song`  
*тут будет полный список атрибутов*
***
### Регистрация на GDPS
Да, это возможно сделать с помощью FruceAPI
```py
import FruceAPI as FRAPI
from asyncio import run

gdps = FRAPI.GDPS('0015') # Подключаем GDPS по ID сервера

async def get_gdps_level():
    account = await gdps.register_account(
        username='FrapiUser', # Имя игрока
        password='RealPassword', # Пароль
        email='example@gmail.com' # Почта
    )

    print(account) # выводит статус создания аккаунта
    # 1 - аккаунт создан успешно
    # -1 - данные вписаны не до конца (например вместо имени пустая строка)
    # -2 - аккаунт с таким именем уже существует
    # -3 - аккаунт с такой почтой уже существует

run(get_gdps_level())
```
Данная функция ничего не возвращает, но создаёт аккаунт в БД, в который можно зайти и играть
