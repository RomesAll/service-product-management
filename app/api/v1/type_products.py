from fastapi import APIRouter, Request
from app.service.products import TypeProductService
from app.utils.helpers import session_dep, pagination_dep

router = APIRouter(prefix="/type-products", tags=["Type products"])

@router.get('/')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = TypeProductService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
def get_records_by_id(request: Request, id: int, session: session_dep):
    result = TypeProductService(session, request.client.host).get_records_by_id(id)
    return {'message': result}