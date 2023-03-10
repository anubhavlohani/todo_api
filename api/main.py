from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import uvicorn
import pymongo

from . import schemas, crud, helpers



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['todo_api']




@app.get("/")
def home():
	return "Ahh, I see you've found this API 🦄. Welcome 🦚"

@app.post("/signup")
def sign_up(user: schemas.User):
	# check if username is taken
	existing_user = crud.get_user(db, user.username)
	if existing_user:
		raise HTTPException(status_code=409, detail='Another user with this username exists. Use a different username.')
	try:
		user.password = helpers.generate_password_hash(user.password)
		crud.create_user(db, user)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new user")
	return {'success': True}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
	auth_data = helpers.authenticate_user(db, form_data)
	return auth_data

@app.get("/todo")
def todo_list(token: str = Depends(oauth2_scheme)):
	user = helpers.decode_token(db, token)
	user_items = crud.user_items(db, user.username)
	return {'todo_items': user_items}

@app.post("/create-item")
def create_item(todo_item: schemas.TodoItem, token: str = Depends(oauth2_scheme)):
	user = helpers.decode_token(db, token)
	# check if user already has an item with this title
	existing_user_item = crud.find_item(db, user.username, todo_item.title)
	if existing_user_item:
		raise HTTPException(status_code=409, detail='An item with the same title already exists. Try using a different title')
	try:
		crud.create_item(db, user, todo_item)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new story")
	return {'success': True}

@app.post("/update-item")
def update_item(item_id: str, item_data: dict, token: str = Depends(oauth2_scheme)):
	user = helpers.decode_token(db, token)
	# check if user owns the item
	collection = db['items']
	item_under_edit = collection.find_one({'_id': item_id})
	if item_under_edit['username'] != user.username:
		raise HTTPException(status_code=401, details="You don't have access to this item")
	try:
		crud.update_item(db, item_id, new_item_data=item_data)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new story")
	return {'success': True}

@app.delete("/delete-item")
def delete_item(item_id: str, token: str = Depends(oauth2_scheme)):
	user = helpers.decode_token(db, token)
	# check if user owns the item
	collection = db['items']
	item_under_edit = collection.find_one({'_id': item_id})
	if item_under_edit['username'] != user.username:
		raise HTTPException(status_code=401, details="You don't have access to this item")
	try:
		crud.delete_item(db, item_id)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new story")
	return {'success': True}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)