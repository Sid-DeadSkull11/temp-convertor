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
    assert b"Temperature Converter" in response.data
    assert b'name="temp"' in response.data
    assert b'value="c_to_f"' in response.data
    assert b'value="f_to_c"' in response.data

def test_valid_conversions_and_boundaries(client):
    res_c_to_f = client.get("/result?type=c_to_f&temp=0")
    assert res_c_to_f.status_code == 200
    assert b"0.0\xc2\xb0C is equal to 32.00\xc2\xb0F" in res_c_to_f.data

    res_f_to_c = client.get("/result?type=f_to_c&temp=212")
    assert res_f_to_c.status_code == 200
    assert b"212.0\xc2\xb0F is equal to 100.00\xc2\xb0C" in res_f_to_c.data

def test_invalid_inputs_and_errors(client):
    res_invalid = client.get("/result?type=c_to_f&temp=abc")
    assert res_invalid.status_code == 200
    assert b"Invalid input parameters." in res_invalid.data

    res_missing = client.get("/result")
    assert b"Invalid input parameters." in res_missing.data