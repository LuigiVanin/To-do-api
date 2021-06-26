from fastapi import APIRouter, Depends, HTTPException, status
from utils.todo import CreateTodo
from sqlalchemy.orm import Session
from config import get_db, pwd_context
from models import *
from utils.permission import get_current_user
from utils.user import CurrentUser
from typing import Optional

todo_router = APIRouter(tags=["todo"])


@todo_router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(request: CreateTodo, db: Session = Depends(get_db),
                currente_user: CurrentUser = Depends(get_current_user)
                ):
    me = db.query(User).filter(User.email == currente_user.email).first()
    todos = db.query(Todo).filter(Todo.title == request.title).all()
    if len(todos) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="já existe um todo com esse título"
        )
    my_todo = Todo(
        title=request.title,
        todo_body=request.body,
        user_id=me.user_id
    )
    db.add(my_todo)
    db.commit()
    db.refresh(my_todo)

    return my_todo

