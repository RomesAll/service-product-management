from app.repositories import ProductsRepository, TypeProductRepository, ProcurementRepository, PaginationParams
from app.schemas.products import *
from sqlalchemy.orm import Session
import uuid

class ProductsService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[ProductsGETSchemas]:
        orm_models = ProductsRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [ProductsGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        return dto_models

    def get_records_by_id(self, id: int) -> ProductsGETSchemas:
        orm_model = ProductsRepository(self.session, self.client).get_records_by_id(id)
        dto_model = ProductsGETSchemas.model_validate(orm_model, from_attributes=True)
        return dto_model

class TypeProductService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[TypeProductGETSchemas]:
        orm_models = TypeProductRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [TypeProductGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        return dto_models

    def get_records_by_id(self, id: int) -> TypeProductGETSchemas:
        orm_models = TypeProductRepository(self.session, self.client).get_records_by_id(id)
        dto_models = TypeProductGETSchemas.model_validate(orm_models, from_attributes=True)
        return dto_models

class ProcurementService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[ProcurementGETSchemas]:
        orm_models = ProcurementRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [ProcurementGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        return dto_models

    def get_records_by_id(self, id: uuid.UUID) -> ProcurementGETSchemas:
        orm_models = ProcurementRepository(self.session, self.client).get_records_by_id(id)
        dto_models = ProcurementGETSchemas.model_validate(orm_models, from_attributes=True)
        return dto_models