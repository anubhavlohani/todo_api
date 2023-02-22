import uuid

from pymongo.database import Database

from . import schemas


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
    query_result = collection.find({'username': username})
    curr_items = [item for item in query_result]
    for item in curr_items:
        item['_id'] = str(item['_id'])
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
    item_data['_id'] = str(uuid.uuid4())
    item_data['username'] = user.username
    insertion_successful = collection.insert_one(item_data)
    return True if insertion_successful else False

# update an item
def update_item(db: Database, item_id: str, new_item_data: dict) -> bool:
    collection = db['items']
    update_query = {"$set": new_item_data}
    update_successful = collection.update_one({'_id': item_id}, update_query)
    return True if update_successful else False

# delete item given it's id
def delete_item(db: Database, item_id: str) -> bool:
    collection = db['items']
    deletion_successful = collection.delete_one({'_id': item_id})
    return True if deletion_successful else False