#app/main.py
from fastapi import FastAPI ,Request
from fastapi.responses import JSONResponse

from app.api.routes import runs
from app.config import setting
from app.api.routes import health
from app.api.routes import auth

app=FastAPI(title=setting.app_name,debug=setting.debug)

@app.exception_handler(ValueError)
async def value_error_handler(request:Request,exc:ValueError):
    return JSONResponse(
        status_code=400,
        content={'detail':f"Invalid input:{str(exc)}"}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request:Request,exc:Exception):
    return JSONResponse(
        status_code=500,
        content={'detail':'Something went wrong,PLease try again'}
    )

app.include_router(health.router)
app.include_router(runs.router,prefix="/api/v1")
app.include_router(auth.router,prefix="/api/v1")
