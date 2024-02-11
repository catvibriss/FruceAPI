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

client = FRAPI.Client("token") # создаём подключение к FruitSpace
# token - это ваш токен на FruitSpace
# НИКОМУ НЕ ДАВАЙТЕ ЭТОТ ТОКЕН (ДАЖЕ КОТУ)!!!
async def about_user(): 
    user = await client.get_user_info() # получаем информацию о пользователе
    print(f"Ваш никнейм: {user['uname']}") # выводим имя пользователя

run(about_user()) # запускаем асинхронную функцию
```
Обратите вниманрие что `get_user_info()` это `corotuine` функция  
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
