from fastapi import APIRouter, Request
from app.service import TypeProductService
from app.schemas import *
from app.utils import session_dep, pagination_dep

router = APIRouter(prefix="/type-products", tags=["Type products"])

@router.get('/')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = TypeProductService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
def get_records_by_id(request: Request, id: int, session: session_dep):
    result = TypeProductService(session, request.client.host).get_records_by_id(id)
    return {'message': result}

@router.post('/')
def create_records(request: Request, dto_model: TypeProductPOSTSchemas, session: session_dep):
    result = TypeProductService(session, request.client.host).create_records(dto_model)
    return {'message': result}

@router.put('/')
def update_records(request: Request, dto_model: TypeProductPUTSchemas, session: session_dep):
    result = TypeProductService(session, request.client.host).update_records(dto_model)
    return {'message': result}

@router.delete('/{id}')
def delete_records(request: Request, id: int, session: session_dep):
    result = TypeProductService(session, request.client.host).delete_records(id)
    return {'message': result}