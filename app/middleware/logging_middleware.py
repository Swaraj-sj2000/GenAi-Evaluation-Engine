#app/middleware/logging_middleware.py

import logging
import json
import uuid
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("eval-engine")
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id=request_id
        start = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000 
        
        logger.info(json.dumps({
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }))
        
        response.headers['X-Request-ID'] = request_id
        return response