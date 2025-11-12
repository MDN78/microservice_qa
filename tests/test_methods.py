import pytest
from http import HTTPStatus

from app.models.User import User
from clients.users_api import UsersApi
from tests.conftest import users_api


# Тест на post: создание. Предусловия: подготовленные тестовые данные
def test_create_user(users_api: UsersApi, new_user):
    response = users_api.create_user(json=new_user)
    assert response.status_code == HTTPStatus.CREATED
    created_user = User.model_validate(response.json())
    assert created_user.email == new_user['email']
    assert created_user.first_name == new_user['first_name']

    users_api.delete_user(created_user.id)


# Тест на patch: изменение. Предусловия: созданный пользователь
@pytest.mark.usefixtures("create_new_user")
@pytest.mark.parametrize("email", ["updated_email@test.com"])
def test_update_user(users_api: UsersApi, create_new_user, email, delete_dummy_user):
    updated_user_info = {'email': email}
    res = users_api.update_user(user_id=create_new_user, json=updated_user_info)
    assert res.status_code == HTTPStatus.OK
    updated_user = User.model_validate(res.json())
    assert updated_user.email == updated_user_info['email']


# Тест на delete: удаление. Предусловия: созданный пользователь
@pytest.mark.usefixtures("create_new_user")
def test_delete_user(users_api: UsersApi, create_new_user):
    response = users_api.delete_user(user_id=create_new_user)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User deleted'


# Тест на 405 ошибку
def test_create_user_non_allowed_method(users_api: UsersApi, new_user):
    response = users_api.create_user_wrong_method(json=new_user)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    data = response.json()
    assert 'Method Not Allowed' in data['detail']


# Тест отправить модель без поля на создание ошибка 422
def test_create_user_without_data(users_api: UsersApi):
    new_user = []
    response = users_api.create_user(json=new_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Тест 404 на удаленного пользователя
@pytest.mark.usefixtures("create_new_user")
def test_get_deleted_user(users_api: UsersApi, create_new_user):
    response = users_api.delete_user(user_id=create_new_user)
    assert response.status_code == HTTPStatus.OK

    response1 = users_api.get_user(create_new_user)
    assert response1.status_code == HTTPStatus.NOT_FOUND
    assert response1.json()['detail'] == 'User not found'
