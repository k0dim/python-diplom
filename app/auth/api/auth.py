# import uuid

# from typing import Annotated, List, Union

# from fastapi import HTTPException, Header
# from sqlalchemy.orm import Session
# import bcrypt

# from auth.database.model import Token

from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.database import crud, schema, model
from auth.main import get_db


SECRET_KEY = '5f1d3488fd4abe64308cec559fb62f6c204acce3f5e3e8aba6b5a0d6bc60a2ff'
ALGORITHN = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


### PASSWORD ### 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hash_password: str):
    return pwd_context(plain_password, hash_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str, model = model.User, db: Session = Depends(get_db)):
    user = crud.get_item_by_email(session=db, model_cls=model, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User is not found. Check your email is correct"
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=404,
            detail="Wrong password"
        )
    return user








# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# def check_password(password_hash: str, password: str) -> bool:
#     return bcrypt.checkpw(password.encode(), password_hash.encode())


# def check_auth(session: Session, token: str) -> Token:
#     try:
#         token = uuid.UUID(token)
#     except (TypeError, ValueError) as error:
#         raise HTTPException(403, "incorrect token")
    
#     token = session.query(Token).get(token)

#     if token is None:
#         raise HTTPException(403, "incorrect token")
    
#     return token