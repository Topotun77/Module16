# Домашнее задание по теме "Валидация данных".
# Цель: научится писать необходимую валидацию для вводимых данных при помощи классов Path и Annotated.
#
# Задача "Аннотация и валидация":
# Допишите валидацию для маршрутов из предыдущей задачи при помощи классов Path и Annotated:
#
# '/user/{user_id}' - функция, выполняемая по этому маршруту, принимает аргумент user_id, для
# которого необходимо написать следующую валидацию:
# 1. Должно быть целым числом
# 2. Ограничено по значению: больше или равно 1 и меньше либо равно 100.
# 3. Описание - 'Enter User ID'
# 4. Пример - '1' (можете подставить свой пример не противоречащий валидации)
#
# '/user' замените на '/user/{username}/{age}' - функция, выполняемая по этому маршруту, принимает
# аргументы username и age, для которых необходимо написать следующую валидацию:
# 1. username - строка, age - целое число.
# 2. username ограничение по длине: больше или равно 5 и меньше либо равно 20.
# 3. age ограничение по значению: больше или равно 18 и меньше либо равно 120.
# 4. Описания для username и age - 'Enter username' и 'Enter age' соответственно.
# 5. Примеры для username и age - 'UrbanUser' и '24' соответственно. (можете подставить свои примеры
# не противоречащие валидации).

from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get('/')
async def welcome() -> str:
    return 'Главная страница'


@app.get('/user/admin')
async def admin() -> str:
    return 'Вы вошли как администратор'


@app.get('/user/{username}/{age}')
async def user_info(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'


@app.get('/user/{user_id}')
async def user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)]) -> str:
    return f'Вы вошли как пользователь № {user_id}'
