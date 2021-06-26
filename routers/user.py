from fastapi import APIRouter, Depends, HTTPException, status
from utils.user import UserScheme, UpdateUser, CurrentUser, ShowUser, ShowMe
from sqlalchemy.orm import Session
from config import get_db, pwd_context
from models import *
from utils.permission import get_current_user
from typing import Optional

user_router = APIRouter(tags=["user"])


@user_router.get("/user/{id}",
                 response_model=ShowUser)
async def get_user(user_id: int, db: Session = Depends(get_db),
                   current_user: UserScheme = Depends(get_current_user)
                   ):
    find_user = db.query(User).filter(User.user_id == user_id)
    if not find_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user com id {}, não existe".format(id)
                            )

    return find_user.first()


@user_router.get("/me",
                 response_model=ShowUser)
async def get_me(db: Session = Depends(get_db),
                 current_user: UserScheme = Depends(get_current_user)):
    me = db.query(User).filter(User.email == current_user.email).first()
    if not me:
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="alguma coisa está errada"
        )

    return me


@user_router.put("/user")
async def update_me(request: UpdateUser, db: Session = Depends(get_db),
                    current_user: CurrentUser = Depends(get_current_user)
                    ):
    to_update = db.query(User).filter(current_user.user_id == User.user_id)

    if not to_update.first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="current user não existe"
        )
    # turn into a function
    data = request.dict()
    update_dict = {}
    for key in request.dict().keys():
        if data[key] != '' and data[key] is not None and data[key] != 0:
            update_dict.update({key: data[key]})

    to_update.update(update_dict)
    db.commit()
    return to_update.first()


@user_router.put("/user/permission/{user_id}",
                 response_model=ShowUser)
async def concede_admin(user_id: Optional[int] = None, db: Session = Depends(get_db),
                        current_user: CurrentUser = Depends(get_current_user)
                        ):

    me = db.query(User).filter(current_user.user_id == User.user_id).first()
    if me.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="você não é admin"
        )

    to_admin = db.query(User).filter(user_id == User.user_id)
    if not to_admin.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user com id {}, não existe".format(user_id)
                            )
    if to_admin.first().role == "admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="{} já é admin".format(user_id)
                            )

    to_admin.update({"role": "admin"})
    db.commit()

    return to_admin.first()


@user_router.delete("/user/{id}",
                    status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(user_id: int,
                   db: Session = Depends(get_db),
                   current_user: CurrentUser = Depends(get_current_user)
                   ) -> None:
    delete = db.query(User).filter(user_id == User.user_id)
    to_delete = delete.first()

    if not to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user não existe"
        )

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="você não é autorizado a fazer essa requisição"
        )
    elif to_delete.user_id == current_user.user_id:
        if len(db.query(User).filter(User.role == 'admin').all()) == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="para que essa conta seja deletada é necessário que exista outro admin"
            )
    delete.delete(synchronize_session=False)
    db.commit()
