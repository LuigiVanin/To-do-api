from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from config import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String)
    age = Column(Integer, default=20)
    password = Column(String)
    role = Column(String, default="normal")
    disable = Column(Boolean, default=False)


class Rel_User_Todo(Base):
    __tablename__ = "user_todo"

    user_id = Column(Integer, ForeignKey("users.user_id"))
    todo_id = Column(Integer, ForeignKey("todos.todo_id"), primary_key=True) # ForeignKey("todo.todo_id")
