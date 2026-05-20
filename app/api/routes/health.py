#app/api/routes/health.py

from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
#from app.db import get_db

router=APIRouter(tags=['health'])

@router.get("/health")
def health():
    return {'status':'ok'}

'''
@router.get("/ready")
def ready(db:Session=Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {'status':'ready','db':'connected'}
    except Exception as e:
        raise HTTPException(status_code=503, detail={'status':'not ready','error':str(e)})
        '''