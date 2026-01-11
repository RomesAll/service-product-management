from fastapi import APIRouter, Request
from app.service import UsersService
from app.schemas import *
from app.dependencies import session_dep, pagination_dep
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.get('/')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = UsersService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
def get_records_by_id(request: Request, id: UUID, session: session_dep):
    result = UsersService(session, request.client.host).get_records_by_id(id)
    return {'message': result}

@router.post('/')
def create_records(request: Request, dto_model: UsersPOSTSchemas, session: session_dep):
    result = UsersService(session, request.client.host).create_records(dto_model)
    return {'message': result}

@router.put('/')
def update_records(request: Request, dto_model: UsersPUTSchemas, session: session_dep):
    result = UsersService(session, request.client.host).update_records(dto_model)
    return {'message': result}

@router.delete('/{id}')
def delete_records(request: Request, id: UUID, session: session_dep):
    result = UsersService(session, request.client.host).delete_records(id)
    return {'message': result}