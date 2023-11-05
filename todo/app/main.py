from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import models, schemas
import crud
from models.database import AsyncSessionLocal, engine
from typing import List

app = FastAPI()


# Установка соединения с БД и создание таблиц (для синхронного просто models.Base.metadata.create_all(bind=engine))
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Добавление todo
@app.post("/todos/add_todo", response_model=schemas.TodoCreate)
async def add_todo(todo_create: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.add_todo(db=db, todo=todo_create)


@app.get("/todos", response_model=List[schemas.Todo])
async def read_todos(db: AsyncSession = Depends(get_db)):
    return await crud.get_todos(db=db, skip=0, limit=10)


# Получение todo по id
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_todo_by_id(db=db, todo_id=todo_id)


# Обновление todo по id
@app.put("/todos/update_{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.update_todo_by_id(db, todo_id=todo_id, todo=todo)
    return db_todo


# Удаление todo по id
@app.delete("/todos/delete_{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.delete_todo_by_id(db, todo_id=todo_id)
    return db_todo
