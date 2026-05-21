#app/api/routes/runs.py

from fastapi import APIRouter,HTTPException,Depends
from app.schemas.run import RunCreate,RunResponse,RunUpdate
from app.repositories import run_repo
from sqlalchemy.orm import Session
from app.database import get_db

router=APIRouter(prefix="/runs",tags=['runs'])

@router.post("/",response_model=RunResponse,status_code=201)
def submit_run(run:RunCreate,db:Session=Depends(get_db)):
    return run_repo.create_run(db,run)

@router.get("/",response_model=list[RunResponse])
def list_runs(db:Session=Depends(get_db)):
    runs=run_repo.get_runs(db)
    return runs

@router.get("/{run_id}",response_model=RunResponse)
def get_run(run_id:int,db:Session=Depends(get_db)):
    run=run_repo.get_run(db,run_id)
    if run is None:
        raise HTTPException(status_code=404,detail={'message':'Run not found'})
    return run

@router.patch("/{run_id}",response_model=RunResponse,status_code=200)
def update_run(run_id:int,run_data:RunUpdate,db:Session=Depends(get_db)):
    run=run_repo.update_run(db,run_id,run_data)
    if run is None:
        raise HTTPException(status_code=404,detail={'message':'Run not found'})
    return run
