from sqlalchemy.exc import IntegrityError
from app.models import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
from app.repositories import ProductsRepository, TypeProductRepository, ProcurementRepository
from contextlib import nullcontext as does_not_raise
import pytest, uuid

class TestProductsRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=2,offset=0), 2, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 3, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProductsOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(1, does_not_raise()), (2, does_not_raise()),
                                                 (3, does_not_raise()), (14, pytest.raises(Exception))])
    def test_get_records_by_id(self, get_test_session, id, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (ProductsOrm(product='test product 1', type_product_id=1, exist=False, provider='provider')),
        (ProductsOrm(product='test product 2', type_product_id=1, exist=True, provider='provider')),
        (ProductsOrm(product='test product 3', type_product_id=1, exist=False, provider='provider'))
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = ProductsRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProductsOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (ProductsOrm(id=1, product='update product 1'), does_not_raise()),
        (ProductsOrm(id=2, product='update product 2'), does_not_raise()),
        (ProductsOrm(id=3, product='update product 2'), pytest.raises(IntegrityError)),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProductsOrm)

    def test_delete_records(self, get_test_session):
        test_object = ProductsOrm(product='test product 4', type_product_id=1, exist=False, provider='provider')
        resalt_test_product = ProductsRepository(get_test_session, '127.0.0.1').create_records(test_object)
        result = ProductsRepository(get_test_session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, ProductsOrm)

class TestTypeProductRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=2,offset=0), 2, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 3, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, TypeProductOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(1, does_not_raise()), (2, does_not_raise()),
                                                 (3, does_not_raise()), (14, pytest.raises(Exception))])
    def test_get_records_by_id(self, get_test_session, id, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (TypeProductOrm(type_product='test type 1')),
        (TypeProductOrm(type_product='test type 2')),
        (TypeProductOrm(type_product='test type 3'))
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = TypeProductRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, TypeProductOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (TypeProductOrm(id=1, type_product='update type 1'), does_not_raise()),
        (TypeProductOrm(id=2, type_product='update type 2'), does_not_raise()),
        (TypeProductOrm(id=3, type_product='update type 2'), pytest.raises(IntegrityError)),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, TypeProductOrm)

    def test_delete_records(self, get_test_session):
        test_object = TypeProductOrm(type_product='test type 4')
        resalt_test_product = TypeProductRepository(get_test_session, '127.0.0.1').create_records(test_object)
        result = TypeProductRepository(get_test_session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, TypeProductOrm)

class TestProcurementRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=2,offset=0), 2, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 3, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProcurementOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [
        (uuid.UUID(f'12345678123456781234567812345671'), does_not_raise()),
        (uuid.UUID(f'12345678123456781234567812345672'), does_not_raise()),
        (uuid.UUID(f'12345678123456781234567812345673'), does_not_raise()),
    ])
    def test_get_records_by_id(self, get_test_session, id: uuid.UUID, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345676'), product_id=1, price=100, count_products=100)),
        (ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345677'), product_id=2, price=100, count_products=100)),
        (ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345678'), product_id=3, price=100, count_products=100)),
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = ProcurementRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProcurementOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345671'), price=434), does_not_raise()),
        (ProcurementOrm(id=uuid.UUID(f'12345678123456781234567812345672'), price=123), does_not_raise()),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProcurementOrm)

    def test_delete_records(self, get_test_session):
        test_object = ProcurementOrm(id=uuid.uuid4(), product_id=1, price=100, count_products=100)
        resalt_test_product = ProcurementRepository(get_test_session, '127.0.0.1').create_records(test_object)
        result = ProcurementRepository(get_test_session, '127.0.0.1').delete_records(resalt_test_product.id)
        assert isinstance(result, ProcurementOrm)