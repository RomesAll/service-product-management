from app.models import *
from app.db import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas import *
import pytest, uuid, random

test_engine = create_engine(url=f'postgresql+psycopg://postgres:qwerty@db_host_test:5432/db_products_test')
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

@pytest.fixture(scope="function")
def pagination():
    return PaginationParams(limit=10, offset=0)

@pytest.fixture(scope='session', autouse=False)
def create_default_records():
    with test_session_maker() as session:
        for i in range(5):
            product_type = TypeProductOrm(type_product=f'type {i}')
            session.add(product_type)
        session.commit()
    with test_session_maker() as session:
        for i in range(5):
            product = ProductsOrm(product=f'product {i}', type_product_id=random.randint(1,5),
                                  exist=True, provider='provider')
            session.add(product)
        session.commit()
    with test_session_maker() as session:
        for i in range(1, 6):
            procurement = ProcurementOrm(id=uuid.UUID(f'1234567812345678123456781234567{i}'),
                                         product_id=random.randint(1,5), price=random.randint(32,100),
                                         count_products=random.randint(1,100))
            session.add(procurement)
        session.commit()

@pytest.fixture(scope='session', autouse=False)
def create_default_users():
    with test_session_maker() as session:
        user_1 = UsersOrm(id=uuid.UUID('12345678123456781234567812345671'), username='roman', email='test1@gmail.com', active=True, password=b'qwerty')
        user_2 = UsersOrm(id=uuid.UUID('12345678123456781234567812345672'), username='nikita', email='test2@gmail.com', active=True, password=b'zxcv')
        user_3 = UsersOrm(id=uuid.UUID('12345678123456781234567812345673'), username='pasha', email='test3@gmail.com', active=False, password=b'ppxc')
        session.add_all([user_1, user_2, user_3])
        session.commit()