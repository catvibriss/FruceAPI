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
import FruceAPI as FRAPI
from asyncio import run

client = FRAPI.Client("698fdf88477-9da6-48e2-8cfa-c8bf719fad93")
async def about_user():
    user = await client.get_user_info()
    print(user['uname'])

run(about_user())
```
я обедать иду 
