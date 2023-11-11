from datetime import datetime, timedelta
from typing import Union, Annotated

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.database import crud, model
from auth.database.schema import schemaUser

from auth.database.database import get_db

SECRET_KEY = '5f1d3488fd4abe64308cec559fb62f6c204acce3f5e3e8aba6b5a0d6bc60a2ff'
ALGORITHN = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict, expires_delata: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delata:
        expire = datetime.utcnow() + expires_delata
    else: 
        expire = datetime.utcnow + timedelta(minutes=15)
    to_encode.update({"ext": str(expire)})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHN)
    return encode_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        db: Annotated[Session, Depends(get_db)],
        # model = model.User
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHN)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        if datetime.utcnow() >= datetime.strptime(payload.get("ext"), '%Y-%m-%d %H:%M:%S.%f'):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_item_by_email(session=db, model_cls=model.User, email=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemaUser.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
