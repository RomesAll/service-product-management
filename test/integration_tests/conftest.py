from fastapi.testclient import TestClient
from app.main import app
from test.conftest import default_object
from app.core.jwt_token import create_access_token, create_refresh_token
from app.schemas import UsersGETSchemas
import pytest

@pytest.fixture(scope="function")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def tokens():
    user = default_object.get('users')[0]
    access_token = create_access_token(UsersGETSchemas.model_validate(user))
    refresh_token = create_refresh_token(UsersGETSchemas.model_validate(user))
    return {'access_token': access_token, 'refresh_token': refresh_token}