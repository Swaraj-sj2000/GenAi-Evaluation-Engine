#app/tasks.py

from app.celery_app import celery_app
import redis
from app.config import setting
from app.database import SessionLocal
from app.repositories.run_repo import get_run
from app.services.eval_service import EvalService
from app.repositories.run_repo import get_golden_runs

@celery_app.task(bind=True,max_retries=3)
def evaluate_run_task(self, run_id:int):
    db=SessionLocal()
    redis_client = redis.Redis.from_url(setting.redis_url, decode_responses=True)   
    try:
        run=get_run(db,run_id)
        if not run:
            print(f"Run {run_id} not found")
            return
        evaluator=EvalService()
        run=evaluator.evaluate(db,run,redis_client)
        threshold = 0.1
        if run.expected_score and run.score < run.expected_score - threshold:
            print(f"REGRESSION DETECTED: run {run.id} scored {run.score}, expected {run.expected_score}")
        return {"run_id": run.id, "status": "completed"}    
            
    except Exception as e:
        db.rollback()
        print(f"Task failed for run {run_id}: {e}")
        raise self.retry(exc=e,countdown=2**self.request.retries)
    finally:
        db.close()
        redis_client.close()


@celery_app.task
def run_regression():
    db = SessionLocal()
    try:
        golden_runs = get_golden_runs(db)
        for run in golden_runs:
            evaluate_run_task.delay(run.id)
    except Exception as e:
        print(f"Regression task failed: {e}")
        raise
    finally:
        db.close()