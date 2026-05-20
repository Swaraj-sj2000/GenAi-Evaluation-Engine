#app/schemas/run.py

from pydantic import BaseModel,Field
from typing import Annotated,Optional

class RunCreate(BaseModel):
    experiment_id:int
    prompt:str
    model_output:str
    model_name:str

class RunResponse(BaseModel):
    id:int
    experiment_id:int
    prompt:str
    model_name:str
    status:str

    