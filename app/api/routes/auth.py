#app/api/routes/auth.py


from sqlalchemy.orm import Session
from app.database import get_db

from fastapi import APIRouter,HTTPException,Depends
from app.schemas.user import UserCreate, UserResponse, LoginData
from app.repositories.user_repo import create_user,get_user_by_username
from app.utils.auth_utils import create_acess_token
from app.utils.password_utils import verify_password
from app.utils.auth_utils import get_current_user

router=APIRouter(prefix="/auth",tags=['auth'])

@router.post('/register',response_model=UserResponse)
def register_user(user_data:UserCreate,db:Session=Depends(get_db)):
    existing_user = get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail={'message':'Username already exists'})
    
    return create_user(db,user_data)

@router.post('/login',tags=['login'])
def login(credentials:LoginData,db:Session=Depends(get_db)):
    user=get_user_by_username(db,credentials.username)

    if user is None or not verify_password(credentials.password,user.hashed_password):
        raise HTTPException(status_code=401,detail={'message':'Invalid username or password'})
    token=create_acess_token(data={'sub':user.username})

    return {'message':'Login successful','token':token,'token_type':'bearer'}

@router.get('/me',response_model=UserResponse)
def get_current_user_info(current_user=Depends(get_current_user)):
    return UserResponse(id=current_user.id,username=current_user.username)