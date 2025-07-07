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
        club1.update({"places": points-1})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert f"Great ! "+str(points-1)+" places booked for "+club1['competition'] == soup.li.text


class TestPlaces:

    def test_should_refuse_more_than_12_once(self, client, club1):
        club1.update({"places": 13})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You can't book more than 12 places" == soup.li.text

    def test_should_refuse_more_12_total(self, client, club1):
        club1.update({"places": 2})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "Great ! 2 places booked for "+club1['competition'] == soup.li.text
        club1.update({"places": 12})
        response = client.post('/purchasePlaces', data=club1)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You already booked 12 places for "+club1['competition'] == soup.li.text
        
