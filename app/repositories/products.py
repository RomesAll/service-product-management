from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.products import ProductsOrm, TypeProduct, ProcurementOrm

class ProductsRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client = client

    def get_all_products(self, pagination):
        query = self.session.query(ProductsOrm).limit(pagination.limit).offset(pagination.offset).all()
        return query
