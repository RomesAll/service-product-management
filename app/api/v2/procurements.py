from fastapi import APIRouter, Request, Depends
from app.service import ProcurementService
from app.schemas import *
from app.dependencies import session_dep, pagination_dep, validate_active_user
from app.decorators import redis_cache
import uuid

router = APIRouter(prefix="/api/v2/procurements", tags=["Procurements"], dependencies=[Depends(validate_active_user)])

@router.get('/')
@redis_cache(expire=60, namespace='products')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = ProcurementService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
@redis_cache(expire=60, namespace='products')
def get_records_by_id(request: Request, id: uuid.UUID, session: session_dep):
    result = ProcurementService(session, request.client.host).get_records_by_id(id)
    return {'message': result}