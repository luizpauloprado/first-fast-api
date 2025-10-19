from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator
from typing import Annotated


# wire_in
class UserIn(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int):
        if v > 100:
            raise ValueError("Age cannot be more than 100")
        return v


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
app = FastAPI()


@app.get("/users", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 10):
    result = list(db.values())
    return result[skip : skip + limit]


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def post_user(user: UserIn):
    next_id = max(db.keys()) + 1
    new_user = UserOut(
        id=next_id,
        name=user.name,
        age=user.age,
    )
    db[next_id] = new_user

    return db[next_id]


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    return db[user_id]


@app.put("/users/{user_id}", response_model=UserOut)
def put_user(user_id: int, user: UserIn):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    updated_user = UserOut(
        id=user_id,
        name=user.name,
        age=user.age,
    )

    db[user_id] = updated_user

    return db[user_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    del db[user_id]


@app.get("/users/search/", response_model=list[UserOut])
def search_user(name: Annotated[str, Query(min_length=2)]):
    result = [
        user for user in db.values() if user.name.lower().startswith(name.lower())
    ]
    return result
