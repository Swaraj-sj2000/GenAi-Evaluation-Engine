#app/tasks.py

from app.celery_app import celery_app
import redis
from app.config import setting
from app.database import SessionLocal
from app.repositories.run_repo import get_run
from app.services.eval_service import EvalService

@celery_app.task
def evaluate_run_task(run_id:int):
    db=SessionLocal()
    redis_client = redis.Redis.from_url(setting.redis_url, decode_responses=True)   
    try:
        run=get_run(db,run_id)
        if not run:
            print(f"Run {run_id} not found")
            return
        evaluator=EvalService()
        run=evaluator.evaluate(db,run,redis_client)
        return {"run_id": run.id, "status": "completed"}    
            
    except Exception as e:
        db.rollback()
        print(f"Task failed for run {run_id}: {e}")
        raise 
    finally:
        db.close()
        redis_client.close()






