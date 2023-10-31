# test_app.py
import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def login_as_user1(client):
    return client.post("/", data={'username': 'user1', 'password': 'pass1'})

def test_login_success(client):
    response = login_as_user1(client)
    assert response.status_code == 302
    assert '/dashboard' in response.headers['Location']

def test_login_failure(client):
    response = client.post("/", data={'username': 'user1', 'password': 'wrongpass'})
    assert response.status_code == 401

def test_dashboard_access(client):
    with client:
        login_as_user1(client)
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert b'00001' in response.data  # Check for account number

def test_logout(client):
    with client:
        login_as_user1(client)
        client.get('/logout')
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/' in response.headers['Location']

def test_create_account(client):
    with client:
        login_as_user1(client)
        response = client.post('/create_account')
        assert response.status_code == 302
        assert '/dashboard' in response.headers['Location']
        response = client.get('/dashboard')
        assert b'00003' in response.data  # Assuming a new account number '00003' is created

def test_transfer_funds(client):
    with client:
        login_as_user1(client)
        # You need to modify this test to match how your transfer function works.
        # This is just a placeholder for the idea.
        response = client.post('/transfer', data={
            'from_account': '00001',
            'to_account': '00002',
            'amount': '50'
        })
        assert response.status_code == 302
        assert '/dashboard' in response.headers['Location']
        response = client.get('/dashboard')
        # Check if the balances have been updated accordingly
        assert b'950' in response.data  # New balance in from_account
        assert b'2550' in response.data  # New balance in to_account
