from pydantic import BaseModel
from typing import Union


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