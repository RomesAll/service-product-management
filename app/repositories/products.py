from sqlalchemy.orm import Session
from app.models.products import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
import uuid

class ProductsRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(ProductsOrm).limit(pagination.limit).offset(pagination.offset).all()
        return query

    def get_records_by_id(self, id: int):
        query = self.session.query(ProductsOrm).filter(ProductsOrm.id == int(id)).one_or_none()
        return query

    def create_records(self, orm_model: ProductsOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        return orm_model.id

class TypeProductRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(TypeProductOrm).limit(pagination.limit).offset(pagination.offset).all()
        return query

    def get_records_by_id(self, id: int):
        query = self.session.query(TypeProductOrm).filter(TypeProductOrm.id == int(id)).one_or_none()
        return query

    def create_records(self, orm_model: TypeProductOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        return orm_model.id

class ProcurementRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(ProcurementOrm).limit(pagination.limit).offset(pagination.offset).all()
        return query

    def get_records_by_id(self, id: uuid.UUID):
        query = self.session.query(ProcurementOrm).filter(ProcurementOrm.id == id).one_or_none()
        return query

    def create_records(self, orm_model: ProcurementOrm):
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        return orm_model.id