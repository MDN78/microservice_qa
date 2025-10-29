from http import HTTPStatus
import pytest
from jsondiff import diff
import requests
import math


def test_total_page_and_size_in_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    data = response.json()
    assert data["total"] == len(data["items"])
    assert response.status_code == HTTPStatus.OK
    assert 'page' in data
    assert 'size' in data


@pytest.mark.parametrize("page, size", [(1, 12), (2, 6), (4, 3)])
def test_page_size(app_url, page, size):
    response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": size})
    data = response.json()
    assert page == data['page']
    assert size == data['size']
    assert len(data["items"]) == size


@pytest.mark.parametrize("size", [12, 6, 3])
def test_expected_pages(app_url, size):
    response = requests.get(f"{app_url}/api/users/", params={"size": size})
    data = response.json()
    expected_pages = math.ceil(data['total'] / size)
    assert data['pages'] == expected_pages
    assert len(data['items']) == size
    assert response.status_code == HTTPStatus.OK


def test_users_in_pages(app_url):
    first_page = {"page": 2, "size": 4}
    second_page = {"page": 3, "size": 4}
    response_1 = requests.get(f"{app_url}/api/users/", params=first_page)
    response_2 = requests.get(f"{app_url}/api/users/", params=second_page)
    data_1 = response_1.json()["items"]
    data_2 = response_2.json()["items"]
    data_difference = diff(data_1, data_2, syntax="symmetric")
    assert data_difference != {}
    assert response_1.status_code == HTTPStatus.OK
    assert response_2.status_code == HTTPStatus.OK
