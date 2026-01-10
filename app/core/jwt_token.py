from app.utils import encode_jwt
from app.core import settings
from abc import abstractmethod
from app.schemas import UsersGETSchemas

@abstractmethod
def create_token(payload: dict, token_type: str, expire_in: int):
    payload.update({'type': token_type})
    token = encode_jwt(payload, expire_in=expire_in)
    return token

def create_access_token(user_info: UsersGETSchemas):
    payload = {
        'sub': str(user_info.id),
        'username': str(user_info.username),
        'active': bool(user_info.active),
    }
    return create_token(payload=payload, expire_in=settings.auth.access_token_exp, token_type='access')

def create_refresh_token(user_info: UsersGETSchemas):
    payload = {
        'sub': str(user_info.id),
    }
    return create_token(payload=payload, expire_in=settings.auth.refresh_token_exp, token_type='refresh')