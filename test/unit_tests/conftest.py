from app.schemas import PaginationParams
from test.conftest import test_session_maker
from app.models import TypeProductOrm, ProductsOrm, ProcurementOrm, UsersOrm
import pytest, uuid, random

DEFAULT_UUID = [uuid.UUID(f'urn:uuid:12345678-1234-5678-1234-56781234567{i}') for i in range(10)]
DEFAULT_ID = [i for i in range(1, 11)]

@pytest.fixture(scope="function")
def pagination():
    return PaginationParams(limit=10, offset=0)

@pytest.fixture(scope='session', autouse=True)
def create_default_records():
    with test_session_maker() as session:
        for key in DEFAULT_ID:
            product_type = TypeProductOrm(id=key, type_product=f'type {key}')
            session.add(product_type)
        session.commit()
    with test_session_maker() as session:
        for key in DEFAULT_ID:
            product = ProductsOrm(id=key, product=f'product {key}', type_product_id=random.choice(DEFAULT_ID),
                                  exist=True, provider='provider')
            session.add(product)
        session.commit()
    with test_session_maker() as session:
        for key in DEFAULT_UUID:
            procurement = ProcurementOrm(id=key, product_id=random.choice(DEFAULT_ID), price=random.randint(32,100),
                                         count_products=random.randint(1,100))
            session.add(procurement)
        session.commit()

@pytest.fixture(scope='session', autouse=True)
def create_users():
    with test_session_maker() as session:
        user_1 = UsersOrm(id=DEFAULT_UUID[0], username='roman', email='test1@gmail.com', active=True, password=b'qwerty')
        user_2 = UsersOrm(id=DEFAULT_UUID[1], username='nikita', email='test2@gmail.com', active=True, password=b'zxcv')
        user_3 = UsersOrm(id=DEFAULT_UUID[2], username='pasha', email='test3@gmail.com', active=False, password=b'ppxc')
        session.add_all([user_1, user_2, user_3])
        session.commit()