from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import Annotated
from app.repositories import UsersRepository
from app.utils import decode_jwt, verify_password
from app.schemas import CredentialUsers, UsersGETSchemas, PaginationParams
from app.db import session_maker
from redis import Redis
from app.core import settings
import jwt

http_bearer = HTTPBearer()

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

def get_redis():
    try:
        redis = Redis.from_url(settings.redis.get_redis_url)
        yield redis
    finally:
        redis.close()

def validate_access_token(token: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if token is None or not token.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate token')
    try:
        payload = decode_jwt(token.credentials)
        token_type = payload.get('type', None)
        if token_type is None or token_type != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type, need access token')
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')
    return payload


def validate_refresh_token(token: HTTPAuthorizationCredentials = Depends(http_bearer), session: Session = Depends(get_session)):
    if token is None or not token.credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
    try:
        payload = decode_jwt(token.credentials)
        token_type = payload.get('type', None)
        if token_type is None or token_type != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type, need refresh token')
        user = UsersRepository(session, client=None).get_records_by_id(payload.get('sub', None))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
        return UsersGETSchemas.model_validate(user, from_attributes=True)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token error')

def validate_user_info(request: Request, cred: CredentialUsers, session: Session = Depends(get_session)):
    user = UsersRepository(session=session, client=request.client.host).get_records_by_username(cred.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    if not verify_password(cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return UsersGETSchemas.model_validate(user, from_attributes=True)

def validate_active_user(payload = Depends(validate_access_token), session: Session = Depends(get_session)):
    user = UsersRepository(session, client=None).get_records_by_id(payload.get('sub'))
    if user is None or user.active == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is not active')
    return payload

session_dep = Annotated[Session, Depends(get_session)]
pagination_dep = Annotated[PaginationParams, Depends(PaginationParams)]
validate_user_info_dep = Annotated[validate_user_info, Depends(validate_user_info)]
validate_active_user_dep = Annotated[validate_active_user, Depends(validate_active_user)]
validate_refresh_token_dep = Annotated[validate_refresh_token, Depends(validate_refresh_token)]