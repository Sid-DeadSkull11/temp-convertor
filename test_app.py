import pytest
from app import app

@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Temperature Converter (Push 1)" in response.data
    assert b'name="celsius"' in response.data

def test_valid_conversions_and_boundaries(client):
    res_freezing = client.get("/result?celsius=0")
    assert res_freezing.status_code == 200
    assert b"0.0\xc2\xb0C is equal to 32.00\xc2\xb0F" in res_freezing.data

    res_boundary = client.get("/result?celsius=-273.15")
    assert b"-273.15\xc2\xb0C is equal to -459.67\xc2\xb0F" in res_boundary.data

def test_invalid_inputs_and_errors(client):
    res_invalid = client.get("/result?celsius=abc")
    assert res_invalid.status_code == 200
    assert b"Invalid input value." in res_invalid.data

    res_missing = client.get("/result")
    assert b"Invalid input value." in res_missing.data
