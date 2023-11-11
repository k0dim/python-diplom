from typing import Annotated

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, status, Request
from sqlalchemy.orm import Session

from auth.database import crud, model, schema
from auth.database.database import Base, engine, get_db
from auth.api import jwtHandler, passwordHandler


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.post("/register/", response_model=schema.schemaUser.User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: schema.schemaUser.UserCreate, db: Session = Depends(get_db)):
    user_params = user.model_dump()
    password = user_params['password']
    del user_params["password"]
    user_create = crud.post_item(session=db, model_cls=model.User, **user_params)
    try:
        psw_params={
            "user_id": user_create.id,
            "password": passwordHandler.get_password_hash(password)
        }
        pass_create = crud.post_item(session=db, model_cls=model.Password, **psw_params)
    except:
        if user_create:
            crud.delete_item(session=db, item=user_create)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail={f"Oops... An internal error occurred, object was deleted"}
        )

    return user_create 


@app.post("/token", response_model=schema.schemaToken.Token, tags=["users"])
async def login_for_accedd_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db = Depends(get_db)
):
    user = passwordHandler.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = jwtHandler.timedelta(minutes=jwtHandler.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwtHandler.create_access_token(
        data={"sub": user.email},
        expires_delata=access_token_expires
    )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
    

@app.get("/user/me", response_model=schema.schemaUser.User, tags=["users"])
def get_me(
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
):
    return current_user


@app.get("/user/{user_id}", response_model=schema.schemaUser.User, status_code=status.HTTP_200_OK, tags=["users"])
def get_user_by_id(
    user_id: int, 
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    db: Session = Depends(get_db), 
):
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    return user


@app.get("/user/email/", response_model=schema.schemaUser.User, status_code=status.HTTP_200_OK, tags=["users"])
def get_user_by_emails(
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    email: str = None,
    db: Session = Depends(get_db)
):
    users = crud.get_item_by_email(session=db, model_cls=model.User, email=email)
    return users


@app.get("/user/all/", response_model=list[schema.schemaUser.User], status_code=status.HTTP_200_OK, tags=["users"])
def get_list_user(
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    users = crud.get_list_items(session=db, model_cls=model.User, skip=skip, limit=limit)
    return users


@app.patch("/user/{user_id}", status_code=status.HTTP_200_OK, tags=["users"])
def patch_user(
    user_id: int,
    user: schema.schemaUser.UserPatch,
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    db: Session = Depends(get_db), 
):
    user_params = user.model_dump(exclude_unset=True)
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    if not user:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User is not found"
                )
    crud.patch_item(session=db, item=user, **user_params)
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    return user


@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(
    user_id: int, 
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    db: Session = Depends(get_db), 
):
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    crud.delete_item(session=db, item=user)


@app.patch("/user/password/{user_id}", status_code=status.HTTP_200_OK, tags=["password"])
def patch_password(
    user_id: int,
    pws_schema: schema.shemaPassword.PasswordPatch,
    current_user: Annotated[schema.schemaUser.User, Depends(jwtHandler.get_current_user)],
    db: Session = Depends(get_db), 
):
    psw_params = pws_schema.model_dump(exclude_unset=True)
    password = crud.get_item_by_joinId(session=db, model_cls=model.Password, id=user_id)
    if not password:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User is not found"
                )
    user_psw = passwordHandler.get_password_hash(psw_params["password"])
    psw_params.update({"password": user_psw})
    crud.patch_item(session=db, item=password, **psw_params)
    user = crud.get_item(session=db, model_cls=model.User, item_id=user_id)
    return user