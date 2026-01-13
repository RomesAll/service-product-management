from sqlalchemy.exc import IntegrityError
from app.models import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
from app.repositories import ProductsRepository, TypeProductRepository, ProcurementRepository
from contextlib import nullcontext as does_not_raise
import pytest, uuid

@pytest.mark.usefixtures('create_default_products')
class TestProductsRepository:

    @pytest.mark.skipif('config.getoption("--run-slow") == "false"')
    @pytest.mark.parametrize("limit, offset, len_array, expectation", [(1, 0, 1, does_not_raise()),
                                                                       (2, 0, 2, does_not_raise()),
                                                                       (5, 0, 3, pytest.raises(Exception))])
    def test_get_all_records(self, session, limit, offset, len_array, expectation):
        with expectation:
            pagination = PaginationParams(limit=limit, offset=offset)
            result = ProductsRepository(session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProductsOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(1, does_not_raise()),
                                                 (2, does_not_raise()),
                                                 (3, does_not_raise()),
                                                 (14, pytest.raises(Exception))])
    def test_get_records_by_id(self, session, id, expectation):
        with expectation:
            result = ProductsRepository(session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("product, type_product_id, exist, provider", [('Test product 1', 1, True, 'provider 1'),
                                                                           ('Test product 2', 2, True, 'provider 2'),
                                                                           ('Test product 3', 3, True, 'provider 3')])
    def test_create_records(self, session, product, type_product_id, exist, provider):
        orm_object = ProductsOrm(product=product, type_product_id=type_product_id, exist=exist, provider=provider)
        result = ProductsRepository(session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProductsOrm)

    @pytest.mark.parametrize("id, product, expectation", [(1, 'update product 1', does_not_raise()),
                                                          (2, 'update product 2', does_not_raise()),
                                                          (3, 'update product 2', pytest.raises(IntegrityError))])
    def test_update_records(self, session, id, product, expectation):
        with expectation:
            orm_object = ProductsOrm(id=id, product=product)
            result = ProductsRepository(session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProductsOrm)

    def test_delete_records(self, session):
        test_object = ProductsOrm(product='Test product 4', type_product_id=1, exist=False, provider='provider 4')
        resalt_test_product = ProductsRepository(session, '127.0.0.1').create_records(test_object)
        result = ProductsRepository(session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, ProductsOrm)

@pytest.mark.usefixtures('create_default_products')
class TestTypeProductRepository:

    @pytest.mark.skipif('config.getoption("--run-slow") == "false"')
    @pytest.mark.parametrize("limit, offset, len_array, expectation", [(1, 0, 1, does_not_raise()),
                                                                       (2, 0, 2, does_not_raise()),
                                                                       (5, 0, 3, pytest.raises(Exception))])
    def test_get_all_records(self, session, limit, offset, len_array, expectation):
        with expectation:
            pagination = PaginationParams(limit=limit, offset=offset)
            result = TypeProductRepository(session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, TypeProductOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(1, does_not_raise()),
                                                 (2, does_not_raise()),
                                                 (3, does_not_raise()),
                                                 (14, pytest.raises(Exception))])
    def test_get_records_by_id(self, session, id, expectation):
        with expectation:
            result = TypeProductRepository(session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("type_product", [('Test type 1', ),
                                              ('Test type 2', ),
                                              ('Test type 3', )])
    def test_create_records(self, session, type_product):
        orm_object = TypeProductOrm(type_product=type_product)
        result = TypeProductRepository(session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, TypeProductOrm)

    @pytest.mark.parametrize("id, type_product, expectation", [(1, 'Update type 1', does_not_raise()),
                                                               (2, 'Update type 2', does_not_raise()),
                                                               (3, 'Update type 2', pytest.raises(IntegrityError))])
    def test_update_records(self, session, id, type_product, expectation):
        with expectation:
            orm_object = TypeProductOrm(id=id, type_product=type_product)
            result = TypeProductRepository(session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, TypeProductOrm)

    def test_delete_records(self, session):
        test_object = TypeProductOrm(type_product='Test type 4')
        resalt_test_product = TypeProductRepository(session, '127.0.0.1').create_records(test_object)
        result = TypeProductRepository(session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, TypeProductOrm)

@pytest.mark.usefixtures('create_default_products')
class TestProcurementRepository:

    @pytest.mark.skipif('config.getoption("--run-slow") == "false"')
    @pytest.mark.parametrize("limit, offset, len_array, expectation", [(1, 0, 1, does_not_raise()),
                                                                    (2, 0, 2, does_not_raise()),
                                                                    (5, 0, 3, pytest.raises(Exception))])
    def test_get_all_records(self, session, limit, offset, len_array, expectation):
        with expectation:
            pagination = PaginationParams(limit=limit, offset=offset)
            result = ProcurementRepository(session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProcurementOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(uuid.UUID(f'12345678123456781234567812345671'), does_not_raise()),
                                                 (uuid.UUID(f'12345678123456781234567812345672'), does_not_raise()),
                                                 (uuid.UUID(f'12345678123456781234567812345673'), does_not_raise()),])
    def test_get_records_by_id(self, session, id: uuid.UUID, expectation):
        with expectation:
            result = ProcurementRepository(session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("id, product_id, price, count_products", [(uuid.UUID(f'12345678123456781234567812345675'), 1, 100, 100),
                                                                       (uuid.UUID(f'12345678123456781234567812345676'), 2, 700, 100),
                                                                       (uuid.UUID(f'12345678123456781234567812345677'), 3, 10, 100)])
    def test_create_records(self, session, id, product_id, price, count_products):
        orm_object = ProcurementOrm(id=id, product_id=product_id, price=price, count_products=count_products)
        result = ProcurementRepository(session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProcurementOrm)

    @pytest.mark.parametrize("id, price, expectation", [(uuid.UUID(f'12345678123456781234567812345671'), 434, does_not_raise()),
                                                        (uuid.UUID(f'12345678123456781234567812345672'), 123, does_not_raise())])
    def test_update_records(self, session, id, price, expectation):
        with expectation:
            orm_object = ProcurementOrm(id=id, price=price)
            result = ProcurementRepository(session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProcurementOrm)

    def test_delete_records(self, session):
        test_object = ProcurementOrm(id=uuid.uuid4(), product_id=1, price=100, count_products=100)
        resalt_test_product = ProcurementRepository(session, '127.0.0.1').create_records(test_object)
        result = ProcurementRepository(session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, ProcurementOrm)