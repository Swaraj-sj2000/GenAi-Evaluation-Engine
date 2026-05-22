#app/auth.py
'''
This module will be specially dedicated to JWT authentication which will be
later followed by OAuth2 authentication.
PLEASE DO NOT MODIFY WITHOUT PERMISSION.
'''
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.run import Run

from fastapi import APIRouter,HTTPException,Depends
from app.schemas.run import RegUser,RunResponse,LoginData
router=APIRouter(prefix="/auth",tags=['auth'])
@router.post('/register',response_model=RunResponse)
def register_user(user_data:RegUser,db:Session=Depends(get_db)):
    pass

@router.post('/login',tags=['login'])
def login(credentials:LoginData,db:Session=Depends(get_db)):
    pass

