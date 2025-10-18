from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


# wire_in
class UserIn(BaseModel):
    name: str
    age: int


# wire_out
class UserOut(BaseModel):
    id: int
    name: str
    age: int


# database
db: dict[int, UserOut] = {
    1: UserOut(id=1, name="Luiz", age=37),
    2: UserOut(id=2, name="Mara", age=65),
    3: UserOut(id=3, name="Beto", age=65),
    4: UserOut(id=4, name="Saulo", age=40),
}


# api
@app.get("/users")
def get_users(skip: int = 0, limit: int = 10):
    result = list(db.values())
    return result[skip : skip + limit]


@app.post("/users")
def post_user(user: UserIn):
    next_id = max(db.keys()) + 1
    new_user = UserOut(
        id=next_id,
        name=user.name,
        age=user.age,
    )
    db[new_user.id] = new_user
    next_id += 1

    return db[new_user.id]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db.keys():
        return "Error"

    return db[user_id]


@app.put("/users/{user_id}")
def put_user(user_id: int, user: UserIn):
    if user_id not in db.keys():
        return "Error"

    updated_user = UserOut(
        id=user_id,
        name=user.name,
        age=user.age,
    )
    db[user_id] = updated_user

    return db[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in db.keys():
        return "Error"

    del db[user_id]


@app.get("/users/search/")
def search_user(name: Annotated[str, Query(min_length=2)]):
    result = [
        user for user in db.values() if user.name.lower().startswith(name.lower())
    ]
    return result
