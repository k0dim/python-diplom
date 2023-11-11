from fastapi import Depends, FastAPI, HTTPException

from database.crud import post_item
from database import schema
from validation import validate
from main import app, get_db

@app.post("/users/register", response_model=schema.schemaUser)
def register():
    # user_data = validate(schema.schemaUser, request.json)
    with Session() as session:
        user_data["password"] = hash_password(user_data["password"])
        user = post_item(session, User, **user_data)
        return jsonify({"id":user.id})
    

def login():
    login_data = validate(schema.schemaUser, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data["email"]).first()
        if User is None or not check_password(user.password, login_data["password"]):
            raise ApiError(401, "Invalid user or password")
        
        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({"token":token.id})
