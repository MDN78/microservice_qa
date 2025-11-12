import pytest
from http import HTTPStatus
from app.models.User import User
from clients.users_api import UsersApi


@pytest.mark.usefixtures("fill_test_data")
def test_users(users_api: UsersApi):
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    users_list = response.json()
    users_dates = users_list["items"]
    for user in users_dates:
        User.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_list = users["items"] if 'items' in users else []
    users_ids = [user["id"] for user in users_list]
    assert len(users_ids) == len(set(users_ids))


def test_user(users_api: UsersApi, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = users_api.get_user(user_id)
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [12345678])
def test_user_nonexistent_values(users_api: UsersApi, user_id):
    response = users_api.get_user(user_id)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, 'fast'])
def test_user_invalid_values(users_api: UsersApi, user_id):
    response = users_api.get_user(user_id)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
