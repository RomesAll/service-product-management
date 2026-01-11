from app.repositories import UsersRepository
from app.models import UsersOrm
from app.schemas import *
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from app.core import settings

class UsersService:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams) -> list[UsersGETSchemas]:
        orm_models = UsersRepository(self.session, self.client).get_all_records(pagination)
        dto_models = [UsersGETSchemas.model_validate(row, from_attributes=True) for row in orm_models]
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_models)
        return dto_models

    def get_records_by_id(self, id: UUID) -> UsersGETSchemas:
        orm_model = UsersRepository(self.session, self.client).get_records_by_id(id)
        dto_model = UsersGETSchemas.model_validate(orm_model, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def create_records(self, dto_model: UsersPOSTSchemas) -> UsersGETSchemas:
        orm_model = UsersOrm(id=uuid4(),**dto_model.model_dump())
        result = UsersRepository(self.session, self.client).create_records(orm_model)
        dto_model = UsersGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def update_records(self, dto_model: UsersPUTSchemas) -> UsersGETSchemas:
        orm_model = UsersOrm(**dto_model.model_dump(exclude_none=True, exclude_defaults=True))
        result = UsersRepository(self.session, self.client).update_records(orm_model)
        dto_model = UsersGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model

    def delete_records(self, id: UUID) -> UsersGETSchemas:
        result = UsersRepository(self.session, self.client).delete_records(id)
        dto_model = UsersGETSchemas.model_validate(result, from_attributes=True)
        settings.logger.debug("client: %s converted the orm model in dto: %s", self.client, dto_model)
        return dto_model