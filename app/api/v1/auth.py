from fastapi import APIRouter, Response
from app.utils import session_dep
from app.core.jwt_token import create_refresh_token, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(response: Response, user_validate):
    access_token = create_access_token(user_validate)
    refresh_token = create_refresh_token(user_validate)
    response.headers["Access-Token"] = f"Bearer {access_token}"
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.post("/register")
def register(response: Response, session: session_dep, user_info):
    result = None
    return {'message': result}

@router.post("/refresh/token")
def refresh_token(response: Response, user_validate):
    access_token = create_access_token(user_validate)
    response.headers["Access-Token"] = f"Bearer {access_token}"
    return {'access_token': access_token}