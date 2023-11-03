from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Todo(Base):
    __tablename__ = "todo"

    todo_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
