import pytest
from server import app
from bs4 import BeautifulSoup


EMAIL1 = "admin@irontemple.com"
EMAIL2 = "john@simplylift.co"

@pytest.fixture
def club1():
    data = {"competition": "Spring Festival", "club": "Iron Temple"}
    return data

@pytest.fixture
def club2():
    data = {"competition": "Fall Classic", "club": "Iron Temple"}
    return data

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def connect(client):
    response = client.post('/showSummary', data={"email": EMAIL1})
    soup = BeautifulSoup(response.data, 'html.parser')
    return soup


