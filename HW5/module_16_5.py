# Домашнее задание по теме "Шаблонизатор Jinja 2."
#
# Цель: научиться взаимодействовать с шаблонами Jinja 2 и использовать их в запросах.
#
# Задача "Список пользователей в шаблоне":
#
# Подготовка:
# 1. Используйте код из предыдущей задачи.
# 2. Скачайте заготовленные шаблоны для их дополнения.
# 3. Шаблоны оставьте в папке templates у себя в проекте.
# 4. Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
#
# Измените и дополните ранее описанные CRUD запросы:
#
# Напишите новый запрос по маршруту '/':
# 1. Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# 2. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также
# передавать в него request и список users. Ключи в словаре для передачи определите
# самостоятельно в соответствии с шаблоном.
#
# Измените get запрос по маршруту '/users' на '/users/{user_id}':
# 1. Функция по этому запросу теперь принимает аргумент request и user_id.
# 2. Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# 3. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также
# передавать в него request и одного из пользователей - user. Ключи в словаре для передачи
# определите самостоятельно в соответствии с шаблоном.

from fastapi import FastAPI, Path, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = None
    username: str = Field(default='User1', min_length=3, max_length=15, description='Введите имя пользователя',
                          example='User')
    age: int = Field(default=21, ge=18, le=120, description='Введите возраст', example=22)


app = FastAPI()
templates = Jinja2Templates(directory='templates')
users: List[User] = [
    User(id=1, username='UrbanUser', age=24),
    User(id=2, username='UrbanTest', age=22),
    User(id=3, username='Capybara', age=60)
]


def get_user_index(user_id: int):
    user_ind = None
    for i in range(len(users)):
        if users[i].id == user_id:
            user_ind = i
            break
    if user_ind is not None:
        return user_ind
    else:
        raise HTTPException(status_code=404, detail=f'User {user_id} was not found')


def delete_user_fn(user_id):
    try:
        user_ind = get_user_index(user_id)
        users.pop(user_ind)
    except HTTPException:
        raise


@app.get('/')
async def users_for_html(request: Request) -> HTMLResponse:
    """
    Список users в виде HTML-документа
    """
    return templates.TemplateResponse('users.html', {'request': request, 'users': users, 'text2': '18'})


@app.get('/users/{user_id}')
async def get_user(request: Request,
                   user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)]) -> HTMLResponse:
    """
    Информация о пользователе
    """
    return templates.TemplateResponse('users.html', {'request': request, 'user': users[get_user_index(user_id)], 'text2': '18'})


@app.get('/delete/{user_id}')
async def delete_user(request: Request,
        user_id: Annotated[int, Path(ge=1, le=100, description='Введите id пользователя', example=1)])\
        -> HTMLResponse:
    """
    Удаление пользователя
    """
    try:
        delete_user_fn(user_id)
        return templates.TemplateResponse('users.html', {'request': request, 'users': users, 'text2': '18'})
    except HTTPException:
        raise


@app.post('/user')
async def add_user(request: Request,
                   username: str | None = Form(default='User1', min_length=3, max_length=15),
                   age: int | None = Form(default=21, ge=18, le=120)) -> HTMLResponse:
    if username != 'User1':
        user_id = users[-1].id + 1 if users != [] else 1
        try:
            users.append(User(id=user_id, username=username, age=age))
        except:
            pass
    return templates.TemplateResponse('users.html', {'request': request, 'users': users, 'text2': '18'})


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
        delete_user_fn(user_id)
        return f'The user {user_id} has been deleted'
    except HTTPException:
        raise
