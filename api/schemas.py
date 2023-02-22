from pydantic import BaseModel
from typing import Optional


'''
ORM schemas
'''
class UserLogin(BaseModel):
  username: str
  password: str

class User(UserLogin):
  name: str

  class Config:
    orm_mode = True

class ReturnUser(BaseModel):
  username: str
  name: str

class TodoItem(BaseModel):
  title: str
  description: Optional[str]
  deadline: str
  status: bool