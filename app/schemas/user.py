#app/schemas/user.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str

class LoginData(BaseModel):
    username:str
    password:str   
