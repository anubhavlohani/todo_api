from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
def sign_up(user: schemas.UserSignUp):
	try:
		user.password = helpers.generate_password_hash(user.password)
		crud.create_user(db, user)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new user")
	return {'success': True}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)