#app/schemas/user.py

from pydantic import BaseModel,Field,field_validator

class UserCreate(BaseModel):
    username:str=Field(...,min_length=3,max_length=50,pattern=r'^[a-zA-Z0-9_]+$')
    password:str=Field(...,min_length=8)


    @field_validator('username')
    @classmethod
    def username_must_not_be_Reserved(cls,v):
        reserved=['admin','root','system']
        if v.lower() in reserved:
            raise ValueError('This username is reserved')
        return v.lower()


class UserResponse(BaseModel):
    id:int
    username:str

class LoginData(BaseModel):
    username:str
    password:str   



