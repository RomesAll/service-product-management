from app.models import UsersOrm
from app.schemas import PaginationParams
from app.repositories import UsersRepository
from contextlib import nullcontext as does_not_raise
import pytest, uuid

@pytest.mark.usefixtures("create_default_users")
class TestUsersRepository:

    @pytest.mark.skipif('config.getoption("--run-slow") == "false"')
    @pytest.mark.parametrize("limit, offset, len_array, expectation", [(1, 0, 1, does_not_raise()),])
    def test_get_all_records(self, session, limit, offset, len_array, expectation):
        with expectation:
            pagination = PaginationParams(limit=limit, offset=offset)
            result = UsersRepository(session, '127.0.0.1').get_all_records(pagination)
            assert all([isinstance(obj, UsersOrm) for obj in result])
            assert len(result) <= len_array

    @pytest.mark.parametrize("id, expectation", [(uuid.UUID('12345678123456781234567812345671'), does_not_raise()),])
    def test_get_records_by_id(self, session, id: uuid.UUID, expectation):
        with expectation:
            result = UsersRepository(session, '127.0.0.1').get_records_by_id(id=id)
            assert result.id == id

    @pytest.mark.parametrize("id, username, email, password, active", [
        (uuid.UUID('12345678123456781234567812345672'), 'nikita', 'nikita@gmail.com', b'qwerty', True),])
    def test_create_records(self, session, id, username, email, password, active):
        orm_object = UsersOrm(id=id, username=username, email=email, password=password, active=active)
        result = UsersRepository(session, '127.0.0.1').create_records(orm_object)
        assert isinstance(result, UsersOrm)

    @pytest.mark.parametrize("id, username", [
        (uuid.UUID('12345678123456781234567812345671'), 'roman'),])
    def test_update_records(self, session, id, username):
        orm_object = UsersOrm(id=id, username=username)
        result = UsersRepository(session, '127.0.0.1').update_records(orm_object)
        assert isinstance(result, UsersOrm)
        assert result.active == True