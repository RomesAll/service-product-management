from app.repositories import TypeProductRepository, ProcurementRepository, ProductsRepository
from app.models import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import *
from sqlalchemy.orm import Session
from app.core import settings
import uuid

class ProductsService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[ProductsGETSchemas]:
        orm_models = ProductsRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [ProductsGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def get_records_by_id(self, id: int) -> ProductsGETSchemas:
        orm_model = ProductsRepository(self.session, self.client).get_records_by_id(id)
        dto_model = ProductsGETSchemas.model_validate(orm_model, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def create_records(self, dto_model: ProductsPOSTSchemas) -> ProductsGETSchemas:
        orm_model = ProductsOrm(**dto_model.model_dump())
        result = ProductsRepository(self.session, self.client).create_records(orm_model)
        dto_model = ProductsGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def update_records(self, dto_model: ProductsPUTSchemas) -> ProductsGETSchemas:
        orm_model = ProductsOrm(**dto_model.model_dump(exclude_none=True, exclude_defaults=True))
        result = ProductsRepository(self.session, self.client).update_records(orm_model)
        dto_model = ProductsGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def delete_records(self, id: int) -> ProductsGETSchemas:
        result = ProductsRepository(self.session, self.client).delete_records(id)
        dto_model = ProductsGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

class TypeProductService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[TypeProductGETSchemas]:
        orm_models = TypeProductRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [TypeProductGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def get_records_by_id(self, id: int) -> TypeProductGETSchemas:
        orm_models = TypeProductRepository(self.session, self.client).get_records_by_id(id)
        dto_models = TypeProductGETSchemas.model_validate(orm_models, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def create_records(self, dto_model: TypeProductPOSTSchemas) -> TypeProductGETSchemas:
        orm_model = TypeProductOrm(**dto_model.model_dump())
        result = TypeProductRepository(self.session, self.client).create_records(orm_model)
        dto_model = TypeProductGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def update_records(self, dto_model: TypeProductPUTSchemas) -> TypeProductGETSchemas:
        orm_model = TypeProductOrm(**dto_model.model_dump(exclude_none=True, exclude_defaults=True))
        result = TypeProductRepository(self.session, self.client).update_records(orm_model)
        dto_model = TypeProductGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def delete_records(self, id: int) -> TypeProductGETSchemas:
        result = TypeProductRepository(self.session, self.client).delete_records(id)
        dto_model = TypeProductGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

class ProcurementService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[ProcurementGETSchemas]:
        orm_models = ProcurementRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [ProcurementGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def get_records_by_id(self, id: uuid.UUID) -> ProcurementGETSchemas:
        orm_models = ProcurementRepository(self.session, self.client).get_records_by_id(id)
        dto_models = ProcurementGETSchemas.model_validate(orm_models, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def create_records(self, dto_model: ProcurementPOSTSchemas) -> ProcurementGETSchemas:
        orm_model = ProcurementOrm(id=uuid.uuid4(), **dto_model.model_dump())
        result = ProcurementRepository(self.session, self.client).create_records(orm_model)
        dto_model = ProcurementGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def update_records(self, dto_model: ProcurementPUTSchemas) -> ProcurementGETSchemas:
        orm_model = ProcurementOrm(**dto_model.model_dump(exclude_none=True, exclude_defaults=True))
        result = ProcurementRepository(self.session, self.client).update_records(orm_model)
        dto_model = ProcurementGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def delete_records(self, id: uuid.UUID) -> ProcurementGETSchemas:
        result = ProcurementRepository(self.session, self.client).delete_records(id)
        dto_model = ProcurementGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model