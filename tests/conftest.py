from http import HTTPStatus
import os
import json
from pathlib import Path

import dotenv
import pytest
from faker import Faker
from clients.users_api import UsersApi


@pytest.fixture(scope="session", autouse=True)
def envs():
    """Set up environment variables"""
    dotenv.load_dotenv()


def pytest_addoption(parser):
    """
    Add options to pytest
    """
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def users_api(env):
    """
    Фикстура по инициализации класса UserApi с передачей переменной окружения
    """
    api = UsersApi(env)
    yield api
    api.session.close()


@pytest.fixture(scope="session")
def app_url():
    """Return app url"""
    return os.getenv("APP_URL", "http://127.0.0.1:8002")


@pytest.fixture
def users(users_api: UsersApi):
    """
    Return users data in JSON format from endpoint api/users.
    Depends on fixture 'app_url'
    """
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def port():
    """Return port number 8002"""
    return 8002


@pytest.fixture(scope="module")
def fill_test_data(users_api: UsersApi):
    """
    Fixture for filling test data.
    Preconditions - add users to database.
    Postconditions - delete created users from database.
    """
    file_path = Path(__file__).parent.parent / "users.json"
    with open(file_path, 'r') as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = users_api.create_user(json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        users_api.delete_user(user_id)


@pytest.fixture
def new_user() -> dict:
    """
    Return new user data. Type dict
    """
    fake = Faker()
    new_user = {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "avatar": fake.image_url()
    }
    return new_user


@pytest.fixture
def create_new_user(users_api: UsersApi, new_user) -> int:
    """
    Create new user with fake dates
    :return: user id
    """
    user = users_api.create_user(json=new_user)
    assert user.status_code == HTTPStatus.CREATED
    return user.json()['id']


@pytest.fixture
def delete_dummy_user(users_api: UsersApi, create_new_user):
    """
    Delete dummy user after testing
    :param users_api: base url
    :param create_new_user: fixture for creating new user, getting user id
    :return: None
    """
    user_id = create_new_user

    yield
    response = users_api.delete_user(user_id)
    assert response.status_code == HTTPStatus.OK
