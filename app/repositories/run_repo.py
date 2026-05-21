#app/repositories/run_repo.py

from sqlalchemy.orm import Session
from app.models.run import Run
from app.schemas.run import RunCreate, RunUpdate

def create_run(db:Session,run_data:RunCreate)->Run:
    db_run=Run(
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

def get_runs(db:Session,skip:int=0,limit:int=10)->list[Run]:
    return db.query(Run).offset(skip).limit(limit).all()

def update_run(db:Session,run_id:int,updates:RunUpdate)->Run|None:
    db_run=get_run(db,run_id)

    if db_run is None:
        return None
    
    for key,value in updates.model_dump(exclude_unset=True).items():
        setattr(db_run,key,value)

    db.commit()
    db.refresh(db_run)
    return db_run