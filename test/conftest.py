from app.models import TypeProductOrm, ProcurementOrm, ProductsOrm, UsersOrm
from app.db import Base
from app.core import settings
from app.db import engine, session_maker
from app.schemas import *
import pytest, uuid

default_object = {
    'type_products': [
        TypeProductOrm(type_product='Фрукты'),
        TypeProductOrm(type_product='Овощи'),
        TypeProductOrm(type_product='Мясо и рыба'),
        TypeProductOrm(type_product='Молочка'),
    ],
    'products': [
        ProductsOrm(product='Говядина', type_product_id=3, exist=True, provider='provider 1'),
        ProductsOrm(product='Свинина', type_product_id=3, exist=True, provider='provider 2'),
        ProductsOrm(product='Молоко', type_product_id=4, exist=True, provider='provider 3'),
        ProductsOrm(product='Огурец', type_product_id=2, exist=True, provider='provider 4'),
    ],
    'procurements': [
        ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345671'), product_id=1, price=10, count_products=30),
        ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345672'), product_id=2, price=40, count_products=70),
        ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345673'), product_id=3, price=90, count_products=100),
        ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345674'), product_id=4, price=84, count_products=400),
    ],
    'users': [
        UsersOrm(id=uuid.UUID('12345678123456781234567812345671'), username='roman',
                 email='roman@gmail.com', active=True, password=b'qwerty'),
    ],
}

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    assert settings.postgres.POSTGRES_MODE == 'TEST'
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield

@pytest.fixture(scope='function')
def session():
    try:
        test_session = session_maker()
        yield test_session
    finally:
        test_session.close()

@pytest.fixture(scope="function")
def pagination():
    return PaginationParams(limit=10, offset=0)

@pytest.fixture(scope='session', autouse=False)
def create_default_products():
    with session_maker() as test_session:
        test_session.add_all(default_object.get('type_products'))
        test_session.add_all(default_object.get('products'))
        test_session.add_all(default_object.get('procurements'))
        test_session.flush()
        test_session.commit()

@pytest.fixture(scope='session', autouse=False)
def create_default_users():
    with session_maker() as test_session:
        test_session.add_all(default_object.get('users'))
        test_session.commit()

def pytest_addoption(parser):
    parser.addoption(
        "--run-slow",
        default="true",
        choices=("true", "false")
    )