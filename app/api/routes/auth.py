#app/api/routes/auth.py

from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime,timezone
from jose import jwt, JWTError
from fastapi import APIRouter,HTTPException,Depends,Request


from app.schemas.user import UserCreate, UserResponse, LoginData
from app.repositories.user_repo import create_user,get_user_by_username
from app.utils.auth_utils import ALGORITHM, create_access_token
from app.utils.password_utils import verify_password
from app.utils.auth_utils import get_current_user
from app.redis_client import get_redis
from app.utils.auth_utils import oauth2_scheme
from app.config import setting
from app.utils.errors import ErrorResponse


router=APIRouter(prefix="/auth",tags=['auth'])

@router.post('/register',response_model=UserResponse)
def register_user(request:Request,user_data:UserCreate,db:Session=Depends(get_db)):
    existing_user = get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail=ErrorResponse(
            error='bad_request',
            message='Username already exists',
            request_id=request.state.request_id,
            status_code=400
        ).model_dump())
    
    return create_user(db,user_data)

@router.post('/login',tags=['login'])
def login(request:Request,credentials:LoginData,db:Session=Depends(get_db)):
    user=get_user_by_username(db,credentials.username)

    if user is None or not verify_password(credentials.password,user.hashed_password):
        raise HTTPException(status_code=401,detail=ErrorResponse(
            error='unauthorized',
            message='Invalid username or password',
            request_id=request.state.request_id,
            status_code=401
        ).model_dump())
    token=create_access_token(data={'sub':user.username})

    return {'message':'Login successful','token':token,'token_type':'bearer'}

@router.post('/logout',tags=['logout'])
def logout(request:Request,token:str=Depends(oauth2_scheme),redis_client=Depends(get_redis)):
    payload = jwt.decode(token, setting.secret_key, algorithms=[ALGORITHM])
    exp=payload.get('exp')
    remaining=int(exp-datetime.now(timezone.utc).timestamp())
    redis_client.set(token,'blacklisted',ex=remaining)
    return {'message':'Logout successful'}

@router.get('/me',response_model=UserResponse)
def get_current_user_info(request:Request,current_user=Depends(get_current_user)):
    return UserResponse(id=current_user.id,username=current_user.username)