from bs4 import BeautifulSoup
from flask import session


def test_should_not_when_try_more_points_than_available(client):
    data = {"competition": "Spring Festival", "club": "Iron Temple", "places": "6"}
    response = client.post('/purchasePlaces', data=data)
    soup = BeautifulSoup(response.data, "html.parser")
    print(soup.li.text)
    assert "You don't have enough points" == soup.li.text

