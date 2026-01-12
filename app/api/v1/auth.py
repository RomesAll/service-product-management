from fastapi import APIRouter, Response, Request
from app.dependencies import session_dep, validate_refresh_token_dep, validate_user_info_dep
from app.core.jwt_token import create_refresh_token, create_access_token
from app.schemas import UsersGETSchemas
from app.service import UsersService

router = APIRouter(prefix="api/v1/auth", tags=["Authentication"])

@router.post("/login")
def login(response: Response, user: validate_user_info_dep):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.headers["Access-Token"] = f"Bearer {access_token}"
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.post("/refresh/token")
def refresh_token(response: Response, user: validate_refresh_token_dep):
    access_token = create_access_token(user)
    response.headers["Access-Token"] = f"Bearer {access_token}"
    return {'access_token': access_token}

@router.post("/register")
def register(request: Request, session: session_dep, user_info: UsersGETSchemas):
    result = UsersService(session, request.client.host).create_records(user_info)
    return {'message': result}
