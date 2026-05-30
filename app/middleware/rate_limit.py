#app/middleware/rate_limit.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis
from app.config import setting

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
        self.redis_client=redis.Redis.from_url(setting.redis_url, decode_responses=True)

    async def dispatch(self,request:Request,call_next):
        client_ip=request.client.host
        key=f"rate_limit:{client_ip}"
        count=self.redis_client.get(key)
        if count is None:
            self.redis_client.set(key,1,ex=60)
        elif int(count)<10:
            self.redis_client.incr(key)
        else:
            return JSONResponse(status_code=429,content={"message":"Too many requests. Please try again later."})
        
        response=await call_next(request)
        return response
