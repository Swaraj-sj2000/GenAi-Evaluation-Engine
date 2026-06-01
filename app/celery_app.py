#app/celery_app.py

from celery import Celery
from celery.schedules import crontab
from app.config import setting

celery_app=Celery(
    'eval-engine',
    broker=setting.redis_url,
    backend=setting.redis_url,
    include=['app.tasks']
)

celery_app.conf.beat_schedule={
    'nightly-regression-run': {
        'task': 'app.tasks.evaluate_run_task',
        'schedule': crontab(hour=2, minute=0)  # Run at 2:00 AM daily
    }
}