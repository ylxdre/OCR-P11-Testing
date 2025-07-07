from ward import fixture, test, using
from server import app
from bs4 import BeautifulSoup


@fixture(scope="global")
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@fixture(scope="global")
def connect(co=test_client):
    response = co.post('/showSummary', data={"email": "admin@irontemple.com"})
    soup = BeautifulSoup(response.data, "html.parser")
    return soup


@test("authentication is ok, welcome well displayed")
def _(client=connect):
    assert client.h2.text == "Welcome, admin@irontemple.com"
   
@test("should be no book link for old competition")
def _(client=connect):
    li = client.find_all("li")
    assert not li[0].a
    assert li[1].a
