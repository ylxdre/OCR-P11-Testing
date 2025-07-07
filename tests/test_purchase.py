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
        # assert "Great-booking complete!" == soup.li.text
        assert f"Great ! "+str(points-1)+" places booked for "+club1['competition'] == soup.li.text


class TestPlaces:

    def test_should_refuse_more_12_once(self, client, club1):
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

class TestDate:

    def test_should_not_display_book_link_for_past_competitions(self, connect):
        li = connect.find_all("li")
        assert not li[0].a
        assert li[1].a


    def test_forged_url_on_past_competition_should_raise_flash(self, client):
        url = '/book/Spring Festival/Iron Temple'
        response = client.get(url)
        assert "You cannot book for a past competition" in response.data.decode()
