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
    user_data = user.dict()
    collection = db['users']
    insertion_successful = collection.insert_one(user_data)
    return True if insertion_successful else False

# return all todo-items for given user
def user_items(db: Database, username: str) -> list[dict]:
    collection = db['items']
    query_result = collection.find({'username': username}, {'_id': 0})
    curr_items = [item for item in query_result]
    return curr_items

# find a specific todo item from a specific user
def find_item(db: Database, username: str, title: str) -> dict:
    collection = db['items']
    query_result = collection.find_one({'username': username, 'title': title})
    return query_result   

# create new todo item for given user
def create_item(db: Database, user: schemas.User, item_data: schemas.TodoItem) -> bool:
    collection = db['items']
    item_data = item_data.dict()
    item_data['username'] = user.username
    insertion_successful = collection.insert_one(item_data)
    return True if insertion_successful else False