from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

# pydantic vs dataclass
# pydantic: integrated to the api, robust validation, helps in doc generation
# dataclasses: preferred for internal data structures, performatic
# = trade-off in Pydantic is a cost for its powerful data validation and parsing features


# wire_in
class UserIn(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)

    def custom_validation(self):
        if self.age > 99:
            raise HTTPException(status_code=500, detail="Age must be less than 99")


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
@app.get("/users", response_model=list[UserOut])
def get_users(skip: int = 0, limit: int = 10):
    result = list(db.values())
    return result[skip : skip + limit]


@app.post("/users", response_model=UserOut)
def post_user(user: UserIn):
    user.custom_validation()

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
        raise HTTPException(status_code=500, detail="User does not exists!")

    return db[user_id]


@app.put("/users/{user_id}", response_model=UserOut)
def put_user(user_id: int, user: UserIn):
    if user_id not in db.keys():
        raise HTTPException(status_code=500, detail="User does not exists!")

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
        raise HTTPException(status_code=500, detail="User does not exists!")

    del db[user_id]


@app.get("/users/search/", response_model=list[UserOut])
def search_user(name: Annotated[str, Query(min_length=2)]):
    result = [
        user for user in db.values() if user.name.lower().startswith(name.lower())
    ]
    return result
