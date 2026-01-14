import time

from app.core import settings
from redis import Redis
from pydantic import BaseModel
from fastapi import Request
import hashlib, json, functools
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

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
                    raw_string = redis_client.get(cache_key)
                    data = str(raw_string, 'utf-8')
                    return Response(content=data, status_code=200, headers={
                        'x-fastapi-cache': 'HIT',
                        'content-type': 'application/json'
                    })
                response = func(*args, **kwargs)
                pre_json_response = jsonable_encoder(response)
                json_response = json.dumps(pre_json_response, ensure_ascii=False)
                redis_client.set(cache_key, json_response, ex=expire)
                return Response(content=json_response, status_code=200, headers={
                    'x-fastapi-cache': 'MISS',
                    'content-type': 'application/json'
                })
        return wrapper
    return decorator