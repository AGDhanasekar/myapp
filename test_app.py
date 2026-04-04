import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_get_todos_empty(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []
