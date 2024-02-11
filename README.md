# FruceAPI
FruceAPI - это удобный инструмент для работы с хостингом FruitSpace  
Данная библиотека *не является официальной* и не создана разработчиками FruitSpace

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

# Работаем с GDPS
> _GDPS - Geometry Dash Private Server_

Напишем программу для получения GDPS сервера
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

# GDPS class
Данный класс позволяет работать с данными из GDPS и не требует введения токена FruitSpace  
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
    
run(get_gdps_user())
```
Поиск игрока по его UID и по его никнейму возвращает одинаковый тип данных - `User` 
*тут будет полный список атрибутов*

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

run(get_gdps_level())
```
Поиск уровня по его ID возвращает тип данных - `Level`
*тут будет полный список атрибутов*

