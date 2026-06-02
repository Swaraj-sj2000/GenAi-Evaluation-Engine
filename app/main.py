#app/main.py
from fastapi import FastAPI ,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.api.routes import runs
from app.config import setting
from app.api.routes import health
from app.api.routes import auth
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware import logging_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    # nothing critical to initialize right now
    print("Eval engine starting up...")
    
    yield  # app runs here, handling requests normally
    
    # --- SHUTDOWN ---
    # runs after in-flight requests complete, before process exits
    print("Eval engine shutting down, closing connections...")
    
    from app.database import engine
    engine.dispose()  # closes all SQLAlchemy pool connections cleanly
    
    import redis as redis_lib
    r = redis_lib.Redis.from_url(setting.redis_url)
    r.connection_pool.disconnect()  # closes Redis pool connections
    
    print("Shutdown complete.")

app=FastAPI(title=setting.app_name,debug=setting.debug)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(logging_middleware.LoggingMiddleware)

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request:Request,exc:RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={'error':'validation_error',
                 'message':str(exc.errors()[0]['msg']),
                 'request_id':request.state.request_id if hasattr(request.state,'request_id') else None,
                 'status_code':422}
    )

@app.exception_handler(Exception)
async def generic_error_handler(request:Request, exc:Exception):
    request_id=getattr(request.state,'request_id',None)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "Something went wrong",
            "request_id": request_id,
            "status_code": 500
        }
    )
app.include_router(health.router)
app.include_router(runs.router,prefix="/api/v1")
app.include_router(auth.router,prefix="/api/v1")

