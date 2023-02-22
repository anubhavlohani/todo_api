from datetime import datetime, timedelta

from fastapi import HTTPException
from pymongo.database import Database

from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from . import crud, schemas
from .config import SECRET_KEY, ALGORITHM



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def generate_password_hash(password) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=1440)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def authenticate_user(db: Database, login_data: schemas.UserLogin) -> dict:
    user = crud.get_user(db, login_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(login_data.password, user['password']):
       raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token_data = {'username': user['username']}
    access_token = create_access_token(token_data)
    user_details = schemas.ReturnUser(
        username=user['username'],
        name=user['name'],
    )
    return {
            "user_details": user_details,
            "access_token": access_token, "token_type": "bearer"
        }