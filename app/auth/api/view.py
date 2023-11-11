from enum import Enum
from typing import Annotated, List, Union

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from auth.database import crud, model, schema
from auth.database.database import SessionLocal, engine

from api.validation import validate
from auth.main import get_db, app
from auth import hash_password, check_auth, check_password


@app.post("/register/", response_model=schema.schemaUser.User)
def create_user(user: schema.schemaUser.UserCreate, db: Session = Depends(get_db)):
    password: str = schema.schemaUser.UserCreate.password
    user_params = user.model_dump()
    del user_params["password"]
    user_create = crud.post_item(session=db, model_cls=model.User, params=user_params)
    password_create = crud.post_item(session=db, model_cls=model.Password, params={
        "user_id": user_create.id,
        "password": hash_password(password)
    })
    return user

@app.post("/login/", response_model=schema.schemaToken)
def login(auth: schema.schemaToken.TokenCreate, db: Session = Depends(get_db)):
    user = crud.get_item_by_email(session=db, model_cls=model.User, email=auth.email)
    if user is None or not check_password(hash_password(auth.password), auth.password):
        raise HTTPException(404, "Invalid user or password")

@app.get("/user/me", response_model=schema.schemaUser.User)
def get_me(
    db: Session = Depends(get_db), 
    token: Annotated[Union[str, None], Header()] = None
):
    token = check_auth(session=db, token=token)
    user = crud.get_item(session=db, model_cls=model.User, item_id=token.user_id)
    return user

@app.get("/user/{user_id}", response_model=schema.schemaUser.User)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    token: Annotated[Union[str, None], Header()] = None
):
    token = check_auth(session=db, token=token)
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    return user

@app.get("/user/all", response_model=schema.schemaUser.UserList)
def get_user_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db), 
    token: Annotated[Union[str, None], Header()] = None
):
    token = check_auth(session=db, token=token)
    users = crud.get_list_items(session=db, model_cls=model.User, skip=skip, limit=limit)
    return users