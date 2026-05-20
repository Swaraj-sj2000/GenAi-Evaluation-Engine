#app/api/routes/runs.py

from fastapi import APIRouter
from app.schemas.run import RunCreate,RunResponse

router=APIRouter(prefix="/runs",tags=['runs'])

@router.post("/",response_model=RunResponse,status_code=201)
def submit_run(run:RunCreate):
    return {
        'id':1,
        'experiment_id':run.experiment_id,
        'prompt':run.prompt,
        'model_name':run.model_name,
        'status':'pending'
    }

@router.get("/{run_id}")
def get_run(run_id:int):
    return {'run_id':run_id,'status':'pending'}