from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.products import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
from app.core import settings
import uuid

class ProductsRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(ProductsOrm).limit(pagination.limit).offset(pagination.offset).all()
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def get_records_by_id(self, id: int):
        query = self.session.query(ProductsOrm).filter(ProductsOrm.id == int(id)).one_or_none()
        if query is None:
            raise HTTPException(status_code=404, detail="Product not found")
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def create_records(self, orm_model: ProductsOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        settings.logger.debug("client: %s added the data: %s", self.client, orm_model)
        return orm_model

    def update_records(self, orm_model: ProductsOrm):
        updating_model = self.session.query(ProductsOrm).filter(ProductsOrm.id == int(orm_model.id)).one_or_none()
        if updating_model is None:
            raise HTTPException(status_code=404, detail="Product not found")
        for key in orm_model.__table__.columns.keys():
            value = orm_model.__dict__.get(key, None)
            if value:
                setattr(updating_model, key, value)
        self.session.commit()
        settings.logger.debug("client: %s refresh the data: %s", self.client, updating_model)
        return updating_model

    def delete_records(self, id: int):
        deleting_model = self.session.query(ProductsOrm).filter(ProductsOrm.id == int(id)).one_or_none()
        if deleting_model is None:
            raise HTTPException(status_code=404, detail="Product not found")
        self.session.delete(deleting_model)
        self.session.commit()
        settings.logger.debug("client: %s deleted the data: %s", self.client, deleting_model)
        return deleting_model

class TypeProductRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(TypeProductOrm).limit(pagination.limit).offset(pagination.offset).all()
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def get_records_by_id(self, id: int):
        query = self.session.query(TypeProductOrm).filter(TypeProductOrm.id == int(id)).one_or_none()
        if query is None:
            raise HTTPException(status_code=404, detail="Type product not found")
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def create_records(self, orm_model: TypeProductOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        settings.logger.debug("client: %s added the data: %s", self.client, orm_model)
        return orm_model

    def update_records(self, orm_model: TypeProductOrm):
        updating_model = self.session.query(TypeProductOrm).filter(TypeProductOrm.id == int(orm_model.id)).one_or_none()
        if updating_model is None:
            raise HTTPException(status_code=404, detail="Type product not found")
        for key in orm_model.__table__.columns.keys():
            value = orm_model.__dict__.get(key, None)
            if value:
                setattr(updating_model, key, value)
        self.session.commit()
        settings.logger.debug("client: %s updated the data: %s", self.client, updating_model)
        return updating_model

    def delete_records(self, id: int):
        deleting_model = self.session.query(TypeProductOrm).filter(TypeProductOrm.id == int(id)).one_or_none()
        if deleting_model is None:
            raise HTTPException(status_code=404, detail="Type product not found")
        self.session.delete(deleting_model)
        self.session.commit()
        settings.logger.debug("client: %s deleted the data: %s", self.client, deleting_model)
        return deleting_model

class ProcurementRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(ProcurementOrm).limit(pagination.limit).offset(pagination.offset).all()
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def get_records_by_id(self, id: uuid.UUID):
        query = self.session.query(ProcurementOrm).filter(ProcurementOrm.id == id).one_or_none()
        if query is None:
            raise HTTPException(status_code=404, detail="Procurement not found")
        settings.logger.debug("client: %s received the data: %s", self.client, query)
        return query

    def create_records(self, orm_model: ProcurementOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        settings.logger.debug("client: %s added the data: %s", self.client, orm_model)
        return orm_model

    def update_records(self, orm_model: ProcurementOrm):
        updating_model = self.session.query(ProcurementOrm).filter(ProcurementOrm.id == orm_model.id).one_or_none()
        if updating_model is None:
            raise HTTPException(status_code=404, detail="Procurement not found")
        for key in orm_model.__table__.columns.keys():
            value = orm_model.__dict__.get(key, None)
            if value:
                setattr(updating_model, key, value)
        self.session.commit()
        settings.logger.debug("client: %s updated the data: %s", self.client, updating_model)
        return updating_model

    def delete_records(self, id: uuid.UUID):
        deleting_model = self.session.query(ProcurementOrm).filter(ProcurementOrm.id == id).one_or_none()
        if deleting_model is None:
            raise HTTPException(status_code=404, detail="Procurement not found")
        self.session.delete(deleting_model)
        self.session.commit()
        settings.logger.debug("client: %s deleted the data: %s", self.client, deleting_model)
        return deleting_model