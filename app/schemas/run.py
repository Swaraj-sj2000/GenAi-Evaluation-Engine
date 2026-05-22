#app/schemas/run.py

from pydantic import BaseModel
from typing import Optional

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

class RunUpdate(BaseModel):
    status:Optional[str]=None
    score:Optional[float]=None
    model_name:Optional[str]=None

class RegUser(BaseModel):
    pass

class LoginData(BaseModel):
    pass