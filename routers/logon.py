from fastapi import APIRouter, Depends, HTTPException, status
from utils.user import UserScheme
from sqlalchemy.orm import Session
from config import get_db, pwd_context
from models import *

logon_router = APIRouter(tags=["logon"])


@logon_router.post("/logon", status_code=status.HTTP_202_ACCEPTED)
async def create_user(request: UserScheme, db: Session = Depends(get_db)):
    new_user = User(name=request.name,
                    email=request.email,
                    age=request.age,
                    password=pwd_context.hash(request.password),
                    role="normal"
                    )

    if not db.query(User).all():
        new_user.role = "admin"

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user