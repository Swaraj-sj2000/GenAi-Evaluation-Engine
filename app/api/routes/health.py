#app/api/routes/health.py

from sqlalchemy import text
from fastapi import APIRouter,Depends, HTTPException,Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.errors import ErrorResponse
router=APIRouter(tags=['health'])

@router.get("/health")
def health():
    return {'status':'ok'}

@router.get("/ready")
def ready(request:Request,db:Session=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {'status':'ready','db':'connected'}
    except Exception as e:
        raise HTTPException(status_code=503, detail=ErrorResponse(
            error='service_unavailable',
            message='Database connection failed',
            request_id=request.state.request_id,
            status_code=503
        ).model_dump())