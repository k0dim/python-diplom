import uuid

from typing import Annotated, List, Union

from fastapi import HTTPException, Header
from sqlalchemy.orm import Session
import bcrypt

from database.model import Token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)


def check_auth(session: Session, header: Annotated[Union[str, None], Header(title='token')] = None) -> Token:
    try:
        token = uuid.UUID(header)
    except (TypeError, ValueError) as error:
        raise HTTPException(403, "incorrect token")
    
    token = session.query(Token).get(token)

    if token is None:
        raise HTTPException(403, "incorrect token")
    
    return token