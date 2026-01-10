from app.db.database import session_maker
from fastapi import Depends
from typing import Annotated
from app.schemas.base import PaginationParams
from sqlalchemy.orm import Session
from app.core import settings

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

session_dep = Annotated[Session, Depends(get_session)]
pagination_dep = Annotated[PaginationParams, Depends(PaginationParams)]