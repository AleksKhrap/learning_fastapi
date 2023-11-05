from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from models import models, schemas
import crud
from models.database import AsyncSessionLocal, engine
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# Кастомный обработчик ошибок
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


# Обработчик глобальных исключений, который "ловит" все необработанные исключения
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Ошибка сервера"}
    )


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


# Получение определенного количества todo
@app.get("/todos", response_model=List[schemas.Todo])
async def read_todos(db: AsyncSession = Depends(get_db)):
    return await crud.get_todos(db=db, skip=0, limit=10)


# Получение todo по id
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await crud.get_todo_by_id(db=db, todo_id=todo_id)
    if todo is None:
        raise CustomException(status_code=404, detail="Запись с таким id не найдена")
    return todo


# Обновление todo по id
@app.put("/todos/update_{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.update_todo_by_id(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise CustomException(status_code=404, detail="Запись с таким id не найдена")
    return db_todo


# Удаление todo по id
@app.delete("/todos/delete_{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.delete_todo_by_id(db, todo_id=todo_id)
    if db_todo is None:
        raise CustomException(status_code=404, detail="Запись с таким id не найдена")
    return db_todo
