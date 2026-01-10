from fastapi import APIRouter, Request
from app.service import ProcurementService, ProcurementPOSTSchemas, ProcurementPUTSchemas
from app.utils.helpers import session_dep, pagination_dep
import uuid

router = APIRouter(prefix="/procurements", tags=["Procurements"])

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