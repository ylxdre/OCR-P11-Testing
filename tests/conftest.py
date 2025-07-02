import pytest
from server import app

EMAIL1 = "admin@irontemple.com"
EMAIL2 = "john@simplylift.co"

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def connect(client):
    response = client.post('/showSummary', data={"email": EMAIL})
    soup = BeautifulSoup(response.data, 'html.parser')

