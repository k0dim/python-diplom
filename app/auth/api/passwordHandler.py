from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.database import crud, model
from auth.database.database import get_db


### PASSWORD ### 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_item_by_email(session=db, model_cls=model.User, email=username)
    passwordDB = crud.get_item_by_joinId(session=db, model_cls=model.Password, id=user.id)
    if not user or not passwordDB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not found. Check your email is correct"
        )
    if not verify_password(password, passwordDB.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password"
        )
    return user