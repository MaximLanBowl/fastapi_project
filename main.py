from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from models.models import User

app = FastAPI(
    title="Info about users"
)

users = [
    {"id": 1, "created_at": "2020-01-01T00:00:00"},
    {"id": 2, "created_at": "2020-01-01T00:00:00"},
    {"id": 3, "created_at": "2020-01-01T00:00:00"},
    {"id": 4, "created_at": "2020-01-01T00:00:00"},
]


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    user_id: int
    username: str


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in users if user.get("id") == user_id]


@app.get("/users/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_user)):
    users = db.query(User).all()
    return users


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


@app.post("/acquire_lock")
async def acquire_lock():
    global lock

    if lock:
        return JSONResponse(status_code=409, content={"message": "already get lock"})

    lock = True
    return {"message": "successfully lock"}


@app.delete("/release_lock")
async def release_lock():
    global lock

    if not lock:
        return JSONResponse(status_code=409, content={"message": "is not lock"})

    lock = False
    return {"message": "Successfully release your lock"}
