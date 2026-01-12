from sqlalchemy.exc import IntegrityError
from app.models import UsersOrm
from app.schemas import PaginationParams
from app.repositories import UsersRepository
from contextlib import nullcontext as does_not_raise
from test.unit_tests.conftest import DEFAULT_UUID
import pytest, uuid

class TestUsersRepository:

    @pytest.mark.parametrize("pagination, len_array, expectation", [
        (PaginationParams(limit=1,offset=0), 1, does_not_raise()),
        (PaginationParams(limit=3,offset=0), 3, does_not_raise()),
        (PaginationParams(limit=3,offset=0), 2, pytest.raises(Exception)),
    ])
    def test_get_all_records(self, get_test_session, pagination, len_array, expectation):
        with expectation:
            result = UsersRepository(get_test_session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, UsersOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [
        (DEFAULT_UUID[0], does_not_raise()),
        (DEFAULT_UUID[1], does_not_raise()),
        (DEFAULT_UUID[2], does_not_raise()),
        (14, pytest.raises(Exception))
    ])
    def test_get_records_by_id(self, get_test_session, id: uuid.UUID, expectation):
        with expectation:
            result = UsersRepository(get_test_session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("orm_object", [
        UsersOrm(id=uuid.uuid4(), username='username test',
                 email='username@gmail.com', password=b'password', active=True),
    ])
    def test_create_records(self, get_test_session, orm_object):
        result = UsersRepository(get_test_session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, UsersOrm)

    @pytest.mark.parametrize("orm_object", [
        UsersOrm(id=DEFAULT_UUID[0], username='update username', active=False),
    ])
    def test_update_records(self, get_test_session, orm_object):
        result = UsersRepository(get_test_session, '127.0.0.1').update_records(orm_object)
        assert isinstance(result, UsersOrm)
        assert result.active == False

    @pytest.mark.parametrize("id", [DEFAULT_UUID[0], DEFAULT_UUID[1]])
    def test_delete_records(self, get_test_session, id):
        result = UsersRepository(get_test_session, '127.0.0.1').delete_records(id)
        assert isinstance(result, UsersOrm)