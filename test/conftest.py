from app.models import *
from app.db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

test_engine = create_engine(url=f'postgresql+psycopg://postgres:qwerty@localhost:5432/db_products_test')
test_session_maker = sessionmaker(bind=test_engine, expire_on_commit=False)

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    yield

@pytest.fixture(scope='function')
def get_test_session():
    try:
        session = test_session_maker()
        yield session
    finally:
        session.close()