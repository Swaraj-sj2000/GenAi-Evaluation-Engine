#app/celery_app.py

from celery import Celery
from app.config import setting

celery_app=Celery(
    'eval-engine',
    broker=setting.redis_url,
    backend=setting.redis_url,
    include=['app.tasks']
)