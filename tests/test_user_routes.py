from unittest.mock import patch, Mock

import pytest
from fastapi.testclient import TestClient

from class_social.main import app


@pytest.fixture
def http_test_client():
    return TestClient(app)


valid_user = {
    "id": 'c1',
    "name": 'Mathias',
    "username": 'mathias',
    "password": 'somepass',
    "email": 'mathias@mathias',
    "created_on": "2023-03-27T00:00:00.000+00:00",
    "is_active": True,
    "address": 'some_address'
}


def test_given_valid_new_user_data_the_system_must_register_the_user_and_return_200_ok(http_test_client):
    with patch('class_social.users.user_controller') as controller_mock:
        controller_mock.get_users = Mock(return_value='users')
        response = http_test_client.post('/users', json=valid_user)
        assert response.status_code == 200


def test_given_invalid_new_user_data_the_system_must_return_422(http_test_client):
    response = http_test_client.post('/users', json={})
    assert response.status_code == 422


def test_given_an_id_for_an_existent_user_system_must_return_200_ok(http_test_client):
    with patch('class_social.users.user_controller') as controller_mock:
        controller_mock.get_user_by_id = Mock(return_value=valid_user)
        response = http_test_client.get('/users/c1')
        assert response.status_code == 200


def test_given_an_nonexistent_user_id_system_must_return_404_ok(http_test_client):
    with patch('class_social.users.user_controller') as controller_mock:
        controller_mock.get_user_by_id = Mock(return_value=None)
        response = http_test_client.get('/users/nonexistent_id')
        assert response.status_code == 404


def test_must_always_return_a_list_of_users_and_200_ok(http_test_client):
    with patch('class_social.users.user_controller') as controller_mock:
        controller_mock.get_users = Mock(return_value=[])
        response = http_test_client.get('/users')
        assert response.status_code == 200

        controller_mock.get_users = Mock(return_value=[valid_user])
        response = http_test_client.get('/users')
        assert response.status_code == 200


