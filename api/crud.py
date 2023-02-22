import datetime
from typing import Union

from fastapi import HTTPException
from pymongo.database import Database

from . import schemas, helpers


# function to search and return true if user exists
def get_user(db: Database, username: str) -> Union[None, dict]:
    collection = db['users']
    user = collection.find_one({'username': username})
    return user

# function to create new user and push to mongoDB
def create_user(db: Database, user: schemas.User) -> bool:
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=409, detail='Another user with this username exists. Use a different username.')
    user_data = user.dict()
    collection = db['users']
    insertion_successful = collection.insert_one(user_data)
    return True if insertion_successful else False