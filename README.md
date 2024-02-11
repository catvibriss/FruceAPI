# FruceAPI
FruceAPI - это удобный инструмент для работы с хостингом FruitSpace  
Данная библиотека *не является официальной* и не создана разработчиками FruitSpace

# С чего начать
Сначала нужно установиьт FruceAPI на ваш компьютер. Для этого пропишите в консоли эту команду
```py
pip install FruceAPI
```
#### Теперь мы можем написать первую программу на FruceAPI
```py
import FruceAPI as FRAPI # импортируем FruceAPI
from asyncio import run # импортируем библиотеку для запуска асинхронной функции

client = FRAPI.Client("token") #создаём подключение к FruitSpace
# token - это ваш токен на FruitSpace
# НИКОМУ НЕ ДАВАЙТЕ ЭТОТ ТОКЕН (ДАЖЕ КОТУ)!!!
async def about_user(): 
    user = await client.get_user_info() # получаем информацию о пользователе
    print(user['uname']) # выводим имя пользователя

run(about_user()) # запускаем асинхзронную функцию
```
Обратите вниманрие что `get_user_info()` это `corotuine` функция  
Если вы всё сделали правильно, то в консоли вы увидите имя вашего аккаунта на FruitSpace
