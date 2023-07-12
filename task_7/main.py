import enum

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title='Управление списком задач')


class Status(enum.Enum):
    to_do = 'to do'
    in_progress = 'in progress'
    done = 'done'


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status


class TaskInput(BaseModel):
    title: str
    description: str
    status: Status


tasks = [
    Task(id=1, title='Title1', description='Task1', status=Status.to_do),
    Task(id=2, title='Title2', description='Task2', status=Status.in_progress),
    Task(id=3, title='Title3', description='Task3', status=Status.done)
]


@app.get('/tasks', response_model=list[Task], summary='Получить список всех задач', tags=['Tasks'])
async def get_tasks():
    return tasks


@app.get('/tasks/{task_id}', response_model=Task, summary='Получить задачу по id', tags=['Tasks'])
async def get_task_by_id(task_id: int):
    found_task = [task for task in tasks if task.id == task_id]
    if found_task:
        return found_task[0]
    raise HTTPException(status_code=404, detail='Task was not found')


@app.post('/tasks', response_model=list[Task], summary='Добавить новую задачу', tags=['Tasks'])
async def create_task(input_task: TaskInput):
    next_id = max(tasks, key=lambda x: x.id).id + 1
    add_task = Task(id=next_id, title=input_task.title, description=input_task.description, status=input_task.status)
    tasks.append(add_task)
    return tasks


@app.put('/tasks/{task_id}', response_model=list[Task], summary='Обновить задачу по id', tags=['Tasks'])
async def change_task(task_id: int, input_task: TaskInput):
    update_task = [task for task in tasks if task.id == task_id]
    if not update_task:
        raise HTTPException(status_code=404, detail='Task was not found')
    update_task[0].title = input_task.title
    update_task[0].description = input_task.description
    update_task[0].status = input_task.status
    return tasks


@app.delete('/tasks/{task_id}', response_model=list[Task], summary='Удалить задачу по id', tags=['Tasks'])
async def delete_task(task_id: int):
    task = [task for task in tasks if task.id == task_id]
    if task:
        tasks.remove(task[0])
        return tasks
    raise HTTPException(status_code=404, detail='Task was not found')


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
