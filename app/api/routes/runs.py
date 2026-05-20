#app/api/routes/runs.py

from fastapi import APIRouter,HTTPException
from app.schemas.run import RunCreate,RunResponse
from app.data.fake_db import fake_db
router=APIRouter(prefix="/runs",tags=['runs'])



@router.post("/",response_model=RunResponse,status_code=201)
def submit_run(run:RunCreate):
    run_id = len(fake_db) + 1
    fake_db[run_id] = {
        'id': run_id,
        'experiment_id': run.experiment_id,
        'prompt': run.prompt,
        'model_name': run.model_name,
        'status': 'pending'
    }
    return fake_db[run_id]

@router.get("/{run_id}",response_model=RunResponse)
def get_run(run_id:int):

    if run_id not in fake_db:
        raise HTTPException(status_code=404,detail="Run not Found")

    return fake_db[run_id]
   
