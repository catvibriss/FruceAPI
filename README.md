# FruceAPI
![PyPI - Downloads](https://img.shields.io/pypi/dm/FruceAPI?color=7d61ff)
![PyPI - License](https://img.shields.io/pypi/l/FruceAPI?color=9767ff)
![PyPI - Version](https://img.shields.io/pypi/v/FruceAPI?color=bf69ff)

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
>>> console output
Ваш никнейм: Nickname
```
Подзравляем! Теперь вы готовы к полноценному использованию FruceAPI!  
Документация: https://miwco.gitbook.io/fruceapi/

P.S. более не поддерживается
