# Домашнее задание по теме "Модели данных Pydantic"
#
# Цель: научиться описывать и использовать Pydantic модель.
#
# Задача "Модель пользователя":
# Подготовка:
# Используйте CRUD запросы из предыдущей задачи.
# Создайте пустой список users = []
# Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
# 1. id - номер пользователя (int)
# 2. username - имя пользователя (str)
# 3. age - возраст пользователя (int)
#
# Измените и дополните ранее описанные 4 CRUD запроса:
#
# get запрос по маршруту '/users' теперь возвращает список users.
# post запрос по маршруту '/user/{username}/{age}', теперь:
# 1. Добавляет в список users объект User.
# 2. id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
# 3. Все остальные параметры объекта User - переданные в функцию username и age соответственно.
# 4. В конце возвращает созданного пользователя.
#
# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
# 1. Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# 2. В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием
# "User was not found" и кодом 404.
#
# delete запрос по маршруту '/user/{user_id}', теперь:
# 1. Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# 2. В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием
# "User was not found" и кодом 404.

from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


# from random import randint


class User(BaseModel):
    id: int = None
    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя пользователя',
                                  example='User')] = 'User'
    age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=22)] = 22


app = FastAPI()
users: List[User] = []


def get_user_index(user_id: int):
    user_ind = None
    for i in range(len(users)):
        if users[i].id == user_id:
            user_ind = i
            break
    if user_ind:
        return user_ind
    else:
        raise HTTPException(status_code=404, detail=f'User {user_id} was not found')


@app.get('/users')
async def get_users() -> List[User]:
    # print(users)
    return users


@app.post('/user/{username}/{age}')
async def add_user(user: User) -> str:
    user_id = users[-1].id + 1 if users != [] else 1
    user.id = user_id
    users.append(user)
    return f'User {user_id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)],
        username: Annotated[
            str, Path(min_length=3, max_length=15, description='Введите имя пользователя', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Введите возраст', example=25)]
) -> str:
    try:
        user_ind = get_user_index(user_id)
        users[user_ind].username = username
        users[user_ind].age = age
        return f'The user {user_id} has been updated'
    except HTTPException:
        raise


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)]) -> str:
    try:
        user_ind = get_user_index(user_id)
        users.pop(user_ind)
        return f'The user {user_id} has been deleted'
    except HTTPException:
        raise
