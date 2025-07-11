from bs4 import BeautifulSoup
from flask import session


class TestPoints:
    '''
    testing both case, book with and without enough points
    '''

    def test_should_nok_when_too_much_points(self, client, connect, club2):
        '''
        test booking an amount of places greater than the available points
        '''
        points = int(connect.span.text)
        club2.update({"places": points+1})
        response = client.post('/purchasePlaces', data=club2)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You don't have enough points" == soup.li.text

    def test_should_ok_when_enough_points(self, client, connect, club2):
        '''
        test booking with enough points
        '''
        points = int(connect.span.text)
        # One remaining point after that :
        club2.update({"places": points-1})
        response = client.post('/purchasePlaces', data=club2)
        soup = BeautifulSoup(response.data, "html.parser")
        assert f"Great ! "+str(points-1)+" places booked for "+club2['competition'] == soup.li.text


class TestPlaces:
    '''
    test the booking limit of 12 places
    '''

    def test_should_refuse_more_12_once(self, client, club2):
        '''
        test to book more than 12 places in one shot
        '''
        club2.update({"places": 13})
        response = client.post('/purchasePlaces', data=club2)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You can't book more than 12 places" == soup.li.text

    def test_should_refuse_more_12_total(self, client, club2):
        '''
        test to book more than 12 places in a two-part reservation
        '''
        club2.update({"places": 1})
        response = client.post('/purchasePlaces', data=club2)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "Great ! 1 places booked for "+club2['competition'] == soup.li.text 
        club2.update({"places": 12})
        response = client.post('/purchasePlaces', data=club2)
        soup = BeautifulSoup(response.data, "html.parser")
        assert "You already booked 12 places for "+club2['competition'] == soup.li.text

        
