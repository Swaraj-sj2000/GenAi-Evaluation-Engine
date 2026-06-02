#app/utils/errors.py

from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error:str
    message:str
    request_id:str|None=None
    status_code:int

