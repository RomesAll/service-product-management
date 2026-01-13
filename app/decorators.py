from app.core import settings
from redis import Redis
from pydantic import BaseModel
from fastapi import Request
import hashlib, json, functools

ALLOWED_OBJECTS_CACHE = (int, float, str, bool, dict, list, BaseModel, Request)

def create_cache_key(func, prefix, namespace, *args, **kwargs):
    first_part = f"{prefix}:{namespace}"
    second_part = f"{func.__name__}:{func.__module__}:{args}"
    for arg in kwargs:
        object = kwargs.get(arg)
        if isinstance(object, Request):
            second_part = second_part + f":{object.client.host}"
        elif isinstance(object, ALLOWED_OBJECTS_CACHE):
            second_part = second_part + f":{object}"
    second_part = second_part.replace(' ','')
    return f"{first_part}:{hashlib.md5(second_part.encode()).hexdigest()}"

def redis_cache(expire: int = 10, namespace: str = 'nonamespace'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = create_cache_key(func, 'fastapi-cache', namespace, *args, **kwargs)
            with Redis.from_url(settings.redis.get_redis_url) as redis_client:
                if redis_client.exists(cache_key):
                    return json.loads(redis_client.get(cache_key))
                response = func(*args, **kwargs)
                redis_client.set(cache_key, json.dumps(response), ex=expire)
                return response
        return wrapper
    return decorator