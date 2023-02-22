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
	return {'todo_items': None}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)