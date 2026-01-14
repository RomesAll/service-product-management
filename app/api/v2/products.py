from fastapi import APIRouter, Request, Depends
from app.service import ProductsService
from app.schemas import *
from app.dependencies import session_dep, pagination_dep, validate_active_user
from app.decorators import redis_cache

router = APIRouter(prefix="/api/v2/products", tags=["Products"], dependencies=[Depends(validate_active_user)])

@router.get('/')
@redis_cache(expire=60, namespace='products')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = ProductsService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
@redis_cache(expire=60, namespace='products')
def get_records_by_id(request: Request, id: int, session: session_dep):
    result = ProductsService(session, request.client.host).get_records_by_id(id)
    return {'message': result}

@router.post('/')
def create_records(request: Request, dto_model: ProductsPOSTSchemas, session: session_dep):
    result = ProductsService(session, request.client.host).create_records(dto_model)
    return {'message': result}

@router.put('/')
def update_records(request: Request, dto_model: ProductsPUTSchemas, session: session_dep):
    result = ProductsService(session, request.client.host).update_records(dto_model)
    return {'message': result}

@router.delete('/{id}')
def delete_records(request: Request, id: int, session: session_dep):
    result = ProductsService(session, request.client.host).delete_records(id)
    return {'message': result}