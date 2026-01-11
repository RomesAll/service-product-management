from app.schemas import PaginationParams
from app.models import UsersOrm
from app.utils import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

class UsersRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client: str = client

    def get_all_records(self, pagination: PaginationParams):
        query = self.session.query(UsersOrm).limit(pagination.limit).offset(pagination.offset).all()
        return query

    def get_records_by_id(self, id: UUID):
        query = self.session.query(UsersOrm).filter(UsersOrm.id == id).one_or_none()
        if query is None:
            raise HTTPException(status_code=404, detail="User not found")
        return query

    def get_records_by_username(self, username: str):
        query = self.session.query(UsersOrm).filter(UsersOrm.username == username).one_or_none()
        if query is None:
            raise HTTPException(status_code=404, detail="User not found")
        return query

    def create_records(self, orm_model: UsersOrm):
        orm_model.password = hash_password(orm_model.password.decode())
        self.session.add(orm_model)
        self.session.flush()
        self.session.commit()
        return orm_model

    def update_records(self, orm_model: UsersOrm):
        updating_model = self.session.query(UsersOrm).filter(UsersOrm.id == orm_model.id).one_or_none()
        if updating_model is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key in orm_model.__table__.columns.keys():
            value = orm_model.__dict__.get(key, None)
            if value:
                setattr(updating_model, key, value)
        self.session.commit()
        return updating_model

    def delete_records(self, id: UUID):
        deleting_model = self.session.query(UsersOrm).filter(UsersOrm.id == id).one_or_none()
        if deleting_model is None:
            raise HTTPException(status_code=404, detail="User not found")
        self.session.delete(deleting_model)
        self.session.commit()
        return deleting_model