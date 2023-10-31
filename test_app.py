# test_app.py
import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client):
    response = client.post("/", data={'username': 'user1', 'password': 'pass1'})
    assert response.status_code == 302
    assert '/dashboard' in response.headers['Location']

def test_login_failure(client):
    response = client.post("/", data={'username': 'user1', 'password': 'wrongpass'})
    assert response.status_code == 401

def test_dashboard_access(client):
    with client:
        client.post("/", data={'username': 'user1', 'password': 'pass1'})
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert b'00001' in response.data  # Check for account number

def test_logout(client):
    with client:
        client.post("/", data={'username': 'user1', 'password': 'pass1'})
        client.get('/logout')
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/' in response.headers['Location']
