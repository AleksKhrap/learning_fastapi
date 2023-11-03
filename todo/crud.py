from sqlalchemy.orm import Session
from models import models, schemas


def add_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, skip: int, limit: int):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()


def update_todo_by_id(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = get_todo_by_id(db, todo_id)
    db_todo.title, db_todo.description, db_todo.completed = todo.title, todo.description, todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo_by_id(db: Session, todo_id: int, todo: schemas.Todo):
    db_todo = get_todo_by_id(db, todo_id)
    db.delete(db_todo)
    db.commit()
    return todo
