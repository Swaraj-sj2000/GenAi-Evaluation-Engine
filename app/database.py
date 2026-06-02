#app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.config import setting
'''
pool_size = (number of worker threads or coroutines) / 2

FastAPI with 40 threadpool threads → pool_size = 10-20
Celery with 8 worker processes → pool_size = 2-4 per worker'''

engine=create_engine(setting.database_url,
                     pool_size=10,
                     max_overflow=20,
                     pool_timeout=30,
                     pool_pre_ping=True)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

