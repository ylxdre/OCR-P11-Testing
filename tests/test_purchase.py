from bs4 import BeautifulSoup
from flask import session


class TestPoints:
    
    def test_should_nok_when_too_much_points(self, client, connect, club1):
        points = int(connect.span.text)
        club1.update({"places": points+1})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You don't have enough points" == soup.li.text

    def test_should_ok_when_enough_points(self, client, connect, club1):
        points = int(connect.span.text)
        data = club1.update({"places": points-1})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "Great-booking complete!" == soup.li.text
