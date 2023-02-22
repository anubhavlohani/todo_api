import datetime
from typing import Union

from fastapi import HTTPException
from pymongo.database import Database

from . import schemas, helpers


# search and return true if user exists
def get_user(db: Database, username: str) -> schemas.User:
    collection = db['users']
    user = collection.find_one({'username': username})
    user = schemas.User(**user)
    return user

# create new user and push to mongoDB
def create_user(db: Database, user: schemas.User) -> bool:
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=409, detail='Another user with this username exists. Use a different username.')
    user_data = user.dict()
    collection = db['users']
    insertion_successful = collection.insert_one(user_data)
    return True if insertion_successful else False

# return all todo-items for given user
def user_items(db: Database, username: str) -> list[dict]:
    collection = db['users']
    curr_items = collection.find({'username': username}, {'_id': 0, 'items': 1})
    curr_items = curr_items[0]['items']
    return curr_items

# create new todo item for given user
def create_item(db: Database, user: schemas.User, item_data: schemas.TodoItem):
    collection = db['users']
    collection.update_one({'username': user.username}, {"$push": {"items": item_data.dict()}})