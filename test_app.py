import os
import pytest

# app.py lê o token durante a importação, então ele precisa ser definido antes.
VALID_TOKEN = "123456"
os.environ["VALID_TOKEN"] = VALID_TOKEN

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_unauthorized_train_endpoint(client):
    response = client.get('/train')
    assert response.status_code == 401

def test_invalid_token_train_endpoint(client):
    response = client.get('/train?token=token-invalido')
    assert response.status_code == 401

def test_train_endpoint(client):
    response = client.get(f'/train?token={VALID_TOKEN}')
    assert response.status_code == 200
    data = response.get_json()

    assert 0.0 <= data["accuracy"] <= 1.0

    report = data["classification_report"]
    for species in ("setosa", "versicolor", "virginica"):
        assert species in report
