from bs4 import BeautifulSoup
from flask import session


def test_should_not_when_try_more_points_than_available(client):
    data = {"competition": "Spring Festival", "club": "Iron Temple", "places": "5"}

    # response = client.post('/book/Spring%20Festival/Iron%20Temple', data=data)
    response = client.post('/purchasePlaces', data=data)
    # print(BeautifulSoup(response.data, "html.parser"))
    print(session)
    #assert "_flashes" in session
    #assert session["_flashes"] == [("message", "You don't have enough points")]
