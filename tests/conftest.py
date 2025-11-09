from http import HTTPStatus
import os
import json
from pathlib import Path

import dotenv
import pytest
import requests
from faker import Faker


@pytest.fixture(scope="session", autouse=True)
def envs():
    """Set up environment variables"""
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    """Return app url"""
    return os.getenv("APP_URL")


@pytest.fixture
def users(app_url):
    """
    Return users data in JSON format from endpoint api/users.
    Depends on fixture 'app_url'
    """
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def port():
    """Return port number 8002"""
    return 8002


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    """
    Fixture for filling test data.
    Preconditions - add users to database.
    Postconditions - delete created users from database.
    """
    file_path = Path(__file__).parent.parent/"users.json"
    with open(file_path, 'r') as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    # with open("users.json") as f:
    #     test_data_users = json.load(f)
    # api_users = []
    # for user in test_data_users:
    #     response = requests.post(f"{app_url}/api/users/", json=user)
    #     api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


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
def create_new_user(app_url, new_user) -> int:
    """
    Create new user with fake dates
    :return: user id
    """
    user = requests.post(f"{app_url}/api/users/", json=new_user)
    assert user.status_code == HTTPStatus.CREATED
    return user.json()['id']


@pytest.fixture
def delete_dummy_user(app_url, create_new_user):
    """
    Delete dummy user after testing
    :param app_url: base url
    :param create_new_user: fixture for creating new user, getting user id
    :return: None
    """
    user_id = create_new_user

    yield

    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
