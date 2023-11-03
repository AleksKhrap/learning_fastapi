from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    completed: bool


class Todo(TodoUpdate):
    todo_id: int

    class Config:
        orm_mode = True
