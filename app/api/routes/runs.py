#app/api/routes/runs.py

from fastapi import APIRouter,HTTPException,Depends,Request
from sqlalchemy.orm import Session

from app.schemas.run import RunCreate,RunResponse,RunUpdate
from app.repositories import run_repo
from app.database import get_db
from app.utils.auth_utils import get_current_user
from app.services.eval_service import EvalService
from app.redis_client import get_redis
from app.tasks import evaluate_run_task
from app.utils.errors import ErrorResponse

router=APIRouter(prefix="/runs",tags=['runs'])

@router.post("/",response_model=RunResponse,status_code=201)
def submit_run(run:RunCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return run_repo.create_run(db,run)

@router.get("/",response_model=list[RunResponse])
def list_runs(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    runs=run_repo.get_runs(db)
    return runs

@router.get("/{run_id}",response_model=RunResponse)
def get_run(request:Request,run_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    run=run_repo.get_run(db,run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error='not_found',
                message=f'Run with ID {run_id} does not exist',
                request_id=request.state.request_id,
                status_code=404).model_dump()
                                 )
    return run

@router.patch("/{run_id}",response_model=RunResponse,status_code=200)
def update_run(request:Request,run_id:int,run_data:RunUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user),redis_client=Depends(get_redis)):
    
    run=run_repo.update_run(db,run_id,run_data,redis_client)
    if run is None:
        raise HTTPException(
                    status_code=404,
                    detail=ErrorResponse(
                        error='not_found',
                        message=f'Run with ID {run_id} does not exist',
                        request_id=request.state.request_id,
                        status_code=404).model_dump()
                                        )    
    return run

@router.post("/{run_id}/evaluate", status_code=202)
def evaluate_run(request:Request,run_id: int, db: Session = Depends(get_db),
                 current_user = Depends(get_current_user)):
    run = run_repo.get_run(db, run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error='not_found',
                message=f'Run with ID {run_id} does not exist',
                request_id=request.state.request_id,
                status_code=404).model_dump()
                                        )
    evaluate_run_task.delay(run_id)
    return {"message": "Evaluation started", "run_id": run_id, "status": "pending"}
    
    
    

 
 