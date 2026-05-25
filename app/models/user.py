#app/models/user.py

from sqlalchemy import Column,Integer,String,Boolean,DateTime,func
from app.database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,server_default=func.now())

