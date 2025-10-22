from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from enum import Enum


# wire_in
class RolesIn(BaseModel):
    allow: list[str]
    deny: list[str] | None = None


class UserIn(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=0)
    roles: RolesIn | None = None

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int):
        if v > 100:
            raise ValueError("Age cannot be more than 100")
        return v


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


# wire_out
class RolesOut(BaseModel):
    allow: list[str]
    deny: list[str] | None = None


class UserOut(BaseModel):
    id: int
    name: str
    age: int
    roles: RolesOut | None = None


# database
db: dict[int, UserOut] = {
    1: UserOut(
        id=1,
        name="Luiz",
        age=37,
        roles=RolesOut(allow=["admin"]),
    ),
    2: UserOut(
        id=2,
        name="Mara",
        age=65,
        roles=RolesOut(allow=["read"], deny=["write"]),
    ),
    3: UserOut(
        id=3,
        name="Beto",
        age=65,
        roles=RolesOut(allow=["read"], deny=["write"]),
    ),
    4: UserOut(id=4, name="Saulo", age=40),
}


# api
app = FastAPI()


@app.get(
    "/users",
    response_model=list[UserOut],
    response_model_exclude_none=True,
)
def get_users(skip: int = 0, limit: int = 10):
    result = list(db.values())
    return result[skip : skip + limit]


@app.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
def post_user(user: UserIn):
    next_id = max(db.keys()) + 1
    new_roles = (
        RolesOut(allow=user.roles.allow, deny=user.roles.deny) if user.roles else None
    )
    new_user = UserOut(
        id=next_id,
        name=user.name,
        age=user.age,
        roles=new_roles,
    )
    db[next_id] = new_user

    return db[next_id]


@app.get(
    "/users/{user_id}",
    response_model=UserOut,
    response_model_exclude_none=True,
)
def get_user(user_id: int):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    return db[user_id]


@app.put(
    "/users/{user_id}",
    response_model=UserOut,
    response_model_exclude_none=True,
)
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


@app.patch(
    "/users/{user_id}",
    response_model=UserOut,
    response_model_exclude_none=True,
)
def patch_user(user_id: int, user: dict):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    saved_user = db[user_id]
    saved_user.name = user["name"] if user.get("name") else saved_user.name
    saved_user.age = user["age"] if user.get("age") else saved_user.age

    db[user_id] = saved_user
    return db[user_id]


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in db.keys():
        raise HTTPException(status_code=404, detail="User not found!")

    del db[user_id]


@app.get(
    "/users/search/",
    response_model=list[UserOut],
    response_model_exclude_none=True,
)
def search_user(
    name: Annotated[str, Query(min_length=2)],
    age: int | None = None,
    order: Order = Order.ASC,
):
    result = [
        user
        for user in db.values()
        if user.name.lower().startswith(name.lower())
        and (age is not None and user.age >= age)
    ]
    sorted_result = sorted(
        result, key=lambda user: user.name, reverse=(order == Order.DESC)
    )

    return sorted_result
