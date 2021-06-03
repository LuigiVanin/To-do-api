from fastapi import APIRouter, Depends, HTTPException, status
from utils.user import UserScheme
from sqlalchemy.orm import Session
from config import get_db, pwd_context
from models import *
from utils.permission import get_current_user

user_router = APIRouter(tags=["user"])


@user_router.get("/user/{id}")
async def get_user(user_id: int, db: Session = Depends(get_db),
                   current_user: UserScheme = Depends(get_current_user)
                   ):
    find_user = db.query(User).filter(User.user_id == user_id)
    if not find_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="blog com id {}, não existe".format(id))

    return find_user.first()
#
# @user_router.put("/user/{id}")
# async def concede_admin(email: str, db: Session = Depends(get_db),
#                         current_user: UserScheme = Depends(get_current_user)
#                         ):
#     db.query(User).filter()
#
