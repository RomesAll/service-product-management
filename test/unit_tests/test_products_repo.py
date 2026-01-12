from sqlalchemy.exc import IntegrityError

from app.models import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
from app.repositories import ProductsRepository, TypeProductRepository, ProcurementRepository
from contextlib import nullcontext as does_not_raise
from test.unit_tests.conftest import DEFAULT_UUID, DEFAULT_ID
import pytest, uuid

class TestProductsRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 5, does_not_raise()),
        (PaginationParams(limit=10,offset=0), 10, does_not_raise()),
        (PaginationParams(limit=10,offset=0), 8, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProductsOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [
        (DEFAULT_ID[0], does_not_raise()),
        (DEFAULT_ID[1], does_not_raise()),
        (DEFAULT_ID[2], does_not_raise()),
        (14, pytest.raises(Exception))
    ])
    def test_get_records_by_id(self, get_test_session, id, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (ProductsOrm(id=DEFAULT_ID[-1] + 1, product='test product 1', type_product_id=DEFAULT_ID[0], exist=False, provider='provider')),
        (ProductsOrm(id=DEFAULT_ID[-1] + 2, product='test product 2', type_product_id=DEFAULT_ID[1], exist=True, provider='provider')),
        (ProductsOrm(id=DEFAULT_ID[-1] + 3, product='test product 3', type_product_id=DEFAULT_ID[2], exist=False, provider='provider'))
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = ProductsRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProductsOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (ProductsOrm(id=DEFAULT_ID[0], product='update product 1'), does_not_raise()),
        (ProductsOrm(id=DEFAULT_ID[1], product='update product 2'), does_not_raise()),
        (ProductsOrm(id=DEFAULT_ID[2], product='update product 2'), pytest.raises(IntegrityError)),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = ProductsRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProductsOrm)

class TestTypeProductRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 5, does_not_raise()),
        (PaginationParams(limit=10,offset=0), 8, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, TypeProductOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [
        (DEFAULT_ID[0], does_not_raise()),
        (DEFAULT_ID[1], does_not_raise()),
        (DEFAULT_ID[2], does_not_raise()),
        (14, pytest.raises(Exception))
    ])
    def test_get_records_by_id(self, get_test_session, id, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (TypeProductOrm(id=DEFAULT_ID[-1] + 1, type_product='test type 11')),
        (TypeProductOrm(id=DEFAULT_ID[-1] + 2, type_product='test type 12')),
        (TypeProductOrm(id=DEFAULT_ID[-1] + 3, type_product='test type 13'))
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = TypeProductRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, TypeProductOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (TypeProductOrm(id=DEFAULT_ID[0], type_product='update type 1'), does_not_raise()),
        (TypeProductOrm(id=DEFAULT_ID[1], type_product='update type 2'), does_not_raise()),
        (TypeProductOrm(id=DEFAULT_ID[2], type_product='update type 2'), pytest.raises(IntegrityError)),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = TypeProductRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, TypeProductOrm)

class TestProcurementRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=5,offset=0), 5, does_not_raise()),
        (PaginationParams(limit=10,offset=0), 8, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, ProcurementOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [
        (DEFAULT_UUID[0], does_not_raise()),
        (DEFAULT_UUID[1], does_not_raise()),
        (DEFAULT_UUID[2], does_not_raise()),
    ])
    def test_get_records_by_id(self, get_test_session, id: uuid.UUID, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        (ProcurementOrm(id=uuid.uuid4(), product_id=DEFAULT_ID[0], price=100, count_products=100)),
        (ProcurementOrm(id=uuid.uuid4(), product_id=DEFAULT_ID[1], price=100, count_products=100)),
        (ProcurementOrm(id=uuid.uuid4(), product_id=DEFAULT_ID[2], price=100, count_products=100)),
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = ProcurementRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, ProcurementOrm)

    @pytest.mark.parametrize("orm_object, expectation", [
        (ProcurementOrm(id=DEFAULT_UUID[0], price=434), does_not_raise()),
        (ProcurementOrm(id=DEFAULT_UUID[1], price=123), does_not_raise()),
    ])
    def test_update_records(self, get_test_session, orm_object, expectation):
        with expectation:
            result = ProcurementRepository(get_test_session, '127.0.0.1').update_records(orm_object)
            assert isinstance(result, ProcurementOrm)