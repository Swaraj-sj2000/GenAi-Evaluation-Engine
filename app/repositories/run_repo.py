#app/repositories/run_repo.py

from sqlalchemy.orm import Session
from app.models.run import Run
from app.schemas.run import RunCreate, RunUpdate
from app.utils.cache_utils import make_cache_key

def create_run(db: Session, run_data: RunCreate, user_id: int | None = None) -> Run:
    db_run=Run(
        user_id=user_id,
        experiment_id=run_data.experiment_id,
        prompt=run_data.prompt,
        model_output=run_data.model_output,
        model_name=run_data.model_name,
    )

    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def get_run(db:Session,run_id:int)->Run|None:
    return db.query(Run).filter(Run.id==run_id).first()

def get_run_for_user(db: Session, run_id: int, user_id: int) -> Run | None:
    return db.query(Run).filter(Run.id == run_id, Run.user_id == user_id).first()

def get_runs(db: Session, skip: int = 0, limit: int = 10, user_id: int | None = None) -> list[Run]:
    query = db.query(Run)
    if user_id is not None:
        query = query.filter(Run.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def update_run(db: Session, run_id: int, updates: RunUpdate, redis_client, user_id: int | None = None) -> Run | None:
    db_run = get_run_for_user(db, run_id, user_id) if user_id is not None else get_run(db, run_id)

    if db_run is None:
        return None
    
    cache_key=make_cache_key(db_run.prompt,db_run.model_output)
    redis_client.delete(cache_key)
    
    for key,value in updates.model_dump(exclude_unset=True).items():
        setattr(db_run,key,value)

    db.commit()
    db.refresh(db_run)
    return db_run


def delete_run(db: Session, run_id: int, user_id: int | None = None) -> bool:
    db_run = get_run_for_user(db, run_id, user_id) if user_id is not None else get_run(db, run_id)
    if db_run is None:
        return False

    db.delete(db_run)
    db.commit()
    return True


def get_golden_runs(db:Session)->list[Run]:
    return db.query(Run).filter(Run.is_golden==True).all()
