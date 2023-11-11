from typing import Union

from fastapi import FastAPI

from database.database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
