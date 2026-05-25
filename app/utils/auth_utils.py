#app/utils/auth_utils.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.database import get_db
from app.config import setting
from app.repositories.user_repo import get_user_by_username


ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def create_acess_token(data:dict)->str:
    to_encode=data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)     
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,setting.secret_key,algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user