#app/redis_client.py

import redis
from app.config import setting

def get_redis():
    r=redis.Redis.from_url(setting.redis_url, decode_responses=True)
    try:
        yield r
    finally:
        pass

