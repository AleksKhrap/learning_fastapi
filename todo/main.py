from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
import crud
from models.database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Добавление todo
@app.post("/todos/add_todo", response_model=schemas.TodoCreate)
async def add_todo(todo_create: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.add_todo(db=db, todo=todo_create)


@app.get("/todos", response_model=List[schemas.Todo])
async def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db=db, skip=0, limit=10)


# Получение todo по id
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo_by_id(db=db, todo_id=todo_id)


# Обновление todo по id
@app.put("/todos/update_{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo_by_id(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Запись с таким id не найдена")
    return db_todo


# Удаление todo по id
@app.delete("/todos/delete_{todo_id}", response_model=schemas.Todo)
async def delete_todo(todo_id: int, todo: schemas.Todo, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo_by_id(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Запись с таким id не найдена")
    return db_todo
