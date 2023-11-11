from typing import Union

import psycopg2
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import desc

from auth.database.model import ORM_MODEL, ORM_MODEL_CLS
from auth.database.schema import SCHEMA_TYPE_CREATE


def get_item(session: Session, model_cls: ORM_MODEL_CLS, item_id: int | str) -> ORM_MODEL:
    item = session.query(model_cls).get(item_id)
    if item is None:
        raise HTTPException(404, f"{model_cls.__name__.lower()} not found")
    return item

def get_item_by_email(session: Session, model_cls: ORM_MODEL_CLS, email) -> ORM_MODEL:
    try:
        item = session.query(model_cls).filter(model_cls.email==email).one()
    except NoResultFound as e:
        raise HTTPException(404, f"User not found")
    if item is None:
        raise HTTPException(404, f"{model_cls.__name__.lower()} not found")
    return item

def get_item_by_joinId(session: Session, model_cls: ORM_MODEL_CLS, id: int) -> ORM_MODEL:
    item = session.query(model_cls).filter(model_cls.user_id==id).one()
    if item is None:
        raise HTTPException(404, f"{model_cls.__name__.lower()} not found")
    return item

def get_list_items(session: Session, model_cls: ORM_MODEL_CLS, skip: int = 0, limit: int = 10) -> ORM_MODEL:
    list_items = session.query(model_cls).offset(skip).limit(limit).all()
    if list_items is None or len(list_items)==0:
        raise HTTPException(404, f"{model_cls.__name__.lower()} not found")
    return list_items

def post_item(session: Session, model_cls: ORM_MODEL_CLS, commit: bool = True, **params) -> ORM_MODEL:
    new_item = model_cls(**params)
    session.add(new_item)
    if commit:
        try:
            session.commit()
            session.refresh(new_item)
        except (IntegrityError, DataError) as error:
            if isinstance(error.orig, psycopg2.errors.UniqueViolation):
                raise HTTPException(409, f"such {model_cls.__name__.lower()} already exists")
            if isinstance(error.orig, psycopg2.errors.StringDataRightTruncation):
                raise HTTPException(409, f"The parameter increases the allowed size")
    return new_item

def patch_item(session: Session, item: ORM_MODEL, commit: bool = True, **params) -> ORM_MODEL:
    for field, value in params.items():
        setattr(item, field, value)
    session.add(item)
    if commit:
        try:
            session.commit()
        except IntegrityError as error:
            if isinstance(error.orig, psycopg2.errors.UniqueViolation):
                raise HTTPException(409, f"attr already exists")
            pass
    return item

def delete_item(session: Session, item: ORM_MODEL, commit: bool = True):
    session.delete(item)
    if commit:
        session.commit()