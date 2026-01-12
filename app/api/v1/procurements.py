from fastapi import APIRouter, Request, Depends
from app.service import ProcurementService
from app.schemas import *
from app.dependencies import session_dep, pagination_dep, validate_active_user
import uuid

router = APIRouter(prefix="api/v1/procurements", tags=["Procurements"], dependencies=[Depends(validate_active_user)])

@router.get('/')
def get_all_records(request: Request, session: session_dep, pagination: pagination_dep):
    result = ProcurementService(session, request.client.host).get_all_records(pagination)
    return {'message': result}

@router.get('/{id}')
def get_records_by_id(request: Request, id: uuid.UUID, session: session_dep):
    result = ProcurementService(session, request.client.host).get_records_by_id(id)
    return {'message': result}

@router.post('/')
def create_records(request: Request, dto_model: ProcurementPOSTSchemas, session: session_dep):
    result = ProcurementService(session, request.client.host).create_records(dto_model)
    return {'message': result}

@router.put('/')
def update_records(request: Request, dto_model: ProcurementPUTSchemas, session: session_dep):
    result = ProcurementService(session, request.client.host).update_records(dto_model)
    return {'message': result}

@router.delete('/{id}')
def delete_records(request: Request, id: uuid.UUID, session: session_dep):
    result = ProcurementService(session, request.client.host).delete_records(id)
    return {'message': result}