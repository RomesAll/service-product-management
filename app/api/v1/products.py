from fastapi import APIRouter, Request
from app.service import ProductsService, ProductsPOSTSchemas
from app.utils.helpers import session_dep, pagination_dep

router = APIRouter(prefix="/products", tags=["Products"])

@router.get('/')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = ProductsService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
def get_records_by_id(request: Request, id: int, session: session_dep):
    result = ProductsService(session, request.client.host).get_records_by_id(id)
    return {'message': result}

@router.post('/')
def create_records(request: Request, dto_model: ProductsPOSTSchemas, session: session_dep):
    result = ProductsService(session, request.client.host).create_records(dto_model)
    return {'message': result}