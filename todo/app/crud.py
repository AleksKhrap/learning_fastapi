from sqlalchemy.ext.asyncio import AsyncSession
from models import models, schemas
from sqlalchemy.future import select
from fastapi import HTTPException


async def add_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def get_todos(db: AsyncSession, skip: int, limit: int):
    todos = await db.execute(select(models.Todo).offset(skip).limit(limit))
    # для синхронного db.query(models.Todo).offset(skip).limit(limit).all()
    return todos.scalars().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int):
    todo = await db.execute(select(models.Todo).filter(models.Todo.todo_id == todo_id))
    if todo is None:
        raise HTTPException(status_code=404, detail="Запись с таким id не найдена")
    # db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    return todo.scalar()


async def update_todo_by_id(db: AsyncSession, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Запись с таким id не найдена")
    db_todo.title, db_todo.description, db_todo.completed = todo.title, todo.description, todo.completed
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def delete_todo_by_id(db: AsyncSession, todo_id: int):
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Запись с таким id не найдена")
    await db.delete(db_todo)
    await db.commit()
    return {"message": "Запись успешно удалена"}
