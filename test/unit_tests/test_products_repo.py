from app.models import ProductsOrm, TypeProductOrm, ProcurementOrm
from app.schemas import PaginationParams
from app.repositories import ProductsRepository, TypeProductRepository, ProcurementRepository
from contextlib import nullcontext as does_not_raise
from test.unit_tests.conftest import DEFAULT_UUID, DEFAULT_ID
from fastapi import HTTPException
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
