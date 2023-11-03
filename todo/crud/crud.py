from sqlalchemy.orm import Session
from todo.models import models, schemas


def add_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.tudo_id == todo_id).first()


def update_todo(db: Session, todo: schemas.TodoUpdate):
    db_todo = models.Todo(title=todo.title, description=todo.description, completed=todo.completed)
    db_todo.title, db_todo.description, db_todo.completed = todo.title, todo.description, todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo: schemas.Todo):
    pass
