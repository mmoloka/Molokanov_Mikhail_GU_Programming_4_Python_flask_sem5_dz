from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field
import uvicorn

app = FastAPI(title='Отображение списка пользователей')
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class UserDump(BaseModel):
    name: str
    email: EmailStr = Field(..., description='Email adress of user')
    password: str = Field(..., min_length=8, pattern="[a-z][A-Z][0-9]",
                          description='Password of the user')


users = [
    User(id=1, name='Ivan', email='user@example1.com', password='eR0eR0eR'),
    User(id=2, name='Petr', email='user@example2.com', password='sC4sC4sC'),
    User(id=3, name='Sidor', email='user@example3.com', password='bM8bM8bM')
]


@app.get('/users', response_class=HTMLResponse, summary='Получить список пользователей', tags=['Users'])
async def get_users(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.post('/user_add', summary='Добавить пользователя', tags=['Users'])
async def add_user(new_user: UserDump):
    new_id = 1
    if users:
        new_id = max(users, key=lambda x: x.id).id + 1
    users.append(User(id=new_id, name=new_user.name, email=new_user.email,
                      password=new_user.password))


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
