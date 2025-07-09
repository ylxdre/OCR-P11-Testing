from flask import session
from bs4 import BeautifulSoup


def test_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_should_display_sorry_with_unknown_email(client):
    email = "test@test.com"
    response = client.post('/showSummary', data={"email": email})
    assert "_flashes" in session
    assert session["_flashes"] == [("message", "Sorry, that email wasn't found")]


def test_shoul_display_page_on_known_email(client):
    email = "admin@irontemple.com"
    response = client.post('/showSummary', data={"email": email})
    soup = BeautifulSoup(response.data, 'html.parser')
    welcome = "Welcome, "+email
    assert welcome in response.data.decode()
