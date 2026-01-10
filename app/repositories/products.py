from sqlalchemy.orm import Session
from app.models.products import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas.base import PaginationParams

class ProductsRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination_params: PaginationParams):
        query = self.session.query(ProductsOrm).limit(pagination_params.limit).offset(pagination_params.offset).all()
        return query

    def get_records_by_id(self, id):
        query = self.session.query(ProductsOrm).filter(ProductsOrm.id == id).one_or_none()
        return query

class TypeProductRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination_params: PaginationParams):
        query = self.session.query(TypeProductOrm).limit(pagination_params.limit).offset(pagination_params.offset).all()
        return query

    def get_records_by_id(self, id):
        query = self.session.query(TypeProductOrm).filter(TypeProductOrm.id == id).one_or_none()
        return query

class ProcurementRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination_params: PaginationParams):
        query = self.session.query(ProcurementOrm).limit(pagination_params.limit).offset(pagination_params.offset).all()
        return query

    def get_records_by_id(self, id):
        query = self.session.query(ProcurementOrm).filter(ProcurementOrm.id == id).one_or_none()
        return query