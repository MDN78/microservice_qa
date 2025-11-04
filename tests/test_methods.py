import pytest
import requests
from http import HTTPStatus

from app.models.User import User


# Тест на post: создание. Предусловия: подготовленные тестовые данные
def test_create_user(app_url, new_user):
    response = requests.post(f"{app_url}/api/users/", json=new_user)
    assert response.status_code == HTTPStatus.CREATED
    created_user = User.model_validate(response.json())
    assert created_user.email == new_user['email']
    assert created_user.first_name == new_user['first_name']

    requests.delete(f"{app_url}/api/users/{created_user.id}")


# Тест на patch: изменение. Предусловия: созданный пользователь
@pytest.mark.usefixtures("create_new_user")
@pytest.mark.parametrize("email", ["updated_email@test.com"])
def test_update_user(app_url, create_new_user, email, delete_dummy_user):
    updated_user_info = {'email': email}
    res = requests.patch(f"{app_url}/api/users/{create_new_user}", json=updated_user_info)
    updated_user = User.model_validate(res.json())
    assert res.status_code == HTTPStatus.OK
    assert updated_user.email == updated_user_info['email']


# Тест на delete: удаление. Предусловия: созданный пользователь
@pytest.mark.usefixtures("create_new_user")
def test_delete_user(app_url, create_new_user):
    response = requests.delete(f"{app_url}/api/users/{create_new_user}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User deleted'


# Тест на 405 ошибку
def test_create_user_non_allowed_method(app_url, new_user):
    response = requests.patch(f"{app_url}/api/users/", json=new_user)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    data = response.json()
    assert 'Method Not Allowed' in data['detail']


# Тест отправить модель без поля на создание ошибка 422
def test_create_user_without_data(app_url):
    new_user = []
    response = requests.post(f"{app_url}/api/users/", json=new_user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Тест 404 на удаленного пользователя
@pytest.mark.usefixtures("create_new_user")
def test_get_deleted_user(app_url, create_new_user):
    response = requests.delete(f"{app_url}/api/users/{create_new_user}")
    assert response.status_code == HTTPStatus.OK
    response1 = requests.get(f"{app_url}/api/users/{create_new_user}")
    assert response1.status_code == HTTPStatus.NOT_FOUND
    assert response1.json()['detail'] == 'User not found'
